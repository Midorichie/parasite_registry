;; Enhanced Parasite Data Registry Smart Contract
;; Version 2.0
;; Contract name: parasite-registry-v2

(define-data-var contract-owner principal tx-sender)

;; Enhanced data structures
(define-map parasite-records
    { record-id: uint }
    {
        parasite-name: (string-utf8 100),
        classification: (string-utf8 50),
        location: (string-utf8 100),
        date-recorded: uint,
        researcher: principal,
        metadata-hash: (buff 32),
        status: (string-utf8 20),  ;; Active, Archived, or Updated
        version: uint,
        previous-version: (optional uint)
    }
)

;; New: Tracking research institutions
(define-map research-institutions
    { institution-id: (string-utf8 50) }
    {
        name: (string-utf8 100),
        verified: bool,
        admin: principal
    }
)

;; New: Mapping researchers to institutions
(define-map researcher-institutions
    principal
    (string-utf8 50)
)

;; New: Geographic regions tracking
(define-map geographic-stats
    { region: (string-utf8 50) }
    {
        total-cases: uint,
        last-updated: uint
    }
)

;; Data vars
(define-data-var total-records uint u0)
(define-data-var total-institutions uint u0)

;; Error codes
(define-constant ERR-NOT-AUTHORIZED (err u100))
(define-constant ERR-INVALID-RECORD (err u101))
(define-constant ERR-INVALID-INSTITUTION (err u102))
(define-constant ERR-NOT-VERIFIED (err u103))

;; New: Register research institution
(define-public (register-institution 
    (institution-id (string-utf8 50))
    (name (string-utf8 100)))
    (let
        ((caller tx-sender))
        (asserts! (is-eq caller contract-owner) ERR-NOT-AUTHORIZED)
        (map-set research-institutions
            { institution-id: institution-id }
            {
                name: name,
                verified: false,
                admin: caller
            }
        )
        (var-set total-institutions (+ (var-get total-institutions) u1))
        (ok true)
    )
)

;; New: Verify research institution
(define-public (verify-institution (institution-id (string-utf8 50)))
    (let
        ((caller tx-sender))
        (asserts! (is-eq caller contract-owner) ERR-NOT-AUTHORIZED)
        (map-set research-institutions
            { institution-id: institution-id }
            (merge (unwrap! (map-get? research-institutions { institution-id: institution-id }) ERR-INVALID-INSTITUTION)
                  { verified: true })
        )
        (ok true)
    )
)

;; Enhanced: Add parasite record with version control
(define-public (add-parasite-record 
    (parasite-name (string-utf8 100))
    (classification (string-utf8 50))
    (location (string-utf8 100))
    (metadata-hash (buff 32)))
    (let
        ((new-id (+ (var-get total-records) u1))
         (researcher-inst (unwrap! (map-get? researcher-institutions tx-sender) ERR-NOT-VERIFIED)))
        ;; Verify researcher's institution
        (asserts! 
            (get verified (unwrap! (map-get? research-institutions { institution-id: researcher-inst }) ERR-INVALID-INSTITUTION))
            ERR-NOT-VERIFIED)
        
        ;; Add record
        (map-set parasite-records
            { record-id: new-id }
            {
                parasite-name: parasite-name,
                classification: classification,
                location: location,
                date-recorded: block-height,
                researcher: tx-sender,
                metadata-hash: metadata-hash,
                status: "Active",
                version: u1,
                previous-version: none
            }
        )
        
        ;; Update geographic stats
        (update-geographic-stats location)
        
        (var-set total-records new-id)
        (ok new-id)
    )
)

;; New: Update existing record (with version control)
(define-public (update-parasite-record
    (record-id uint)
    (parasite-name (string-utf8 100))
    (classification (string-utf8 50))
    (location (string-utf8 100))
    (metadata-hash (buff 32)))
    (let
        ((existing-record (unwrap! (map-get? parasite-records { record-id: record-id }) ERR-INVALID-RECORD))
         (new-id (+ (var-get total-records) u1)))
        
        ;; Only original researcher or institution admin can update
        (asserts! (or
            (is-eq tx-sender (get researcher existing-record))
            (is-institution-admin tx-sender)
        ) ERR-NOT-AUTHORIZED)
        
        ;; Archive old version
        (map-set parasite-records
            { record-id: record-id }
            (merge existing-record { status: "Archived" })
        )
        
        ;; Create new version
        (map-set parasite-records
            { record-id: new-id }
            {
                parasite-name: parasite-name,
                classification: classification,
                location: location,
                date-recorded: block-height,
                researcher: tx-sender,
                metadata-hash: metadata-hash,
                status: "Active",
                version: (+ (get version existing-record) u1),
                previous-version: (some record-id)
            }
        )
        
        (var-set total-records new-id)
        (ok new-id)
    )
)

;; Helper function: Update geographic stats
(define-private (update-geographic-stats (region (string-utf8 50)))
    (let
        ((current-stats (default-to { total-cases: u0, last-updated: u0 }
            (map-get? geographic-stats { region: region }))))
        (map-set geographic-stats
            { region: region }
            {
                total-cases: (+ (get total-cases current-stats) u1),
                last-updated: block-height
            }
        )
    )
)

;; Enhanced read functions
(define-read-only (get-parasite-record-history (record-id uint))
    (let
        ((record (unwrap! (map-get? parasite-records { record-id: record-id }) ERR-INVALID-RECORD)))
        (match (get previous-version record)
            prev-id (list
                record
                (unwrap! (map-get? parasite-records { record-id: prev-id }) ERR-INVALID-RECORD)
            )
            record
        )
    )
)

(define-read-only (get-geographic-stats (region (string-utf8 50)))
    (map-get? geographic-stats { region: region })
)

(define-read-only (get-institution-details (institution-id (string-utf8 50)))
    (map-get? research-institutions { institution-id: institution-id })
)