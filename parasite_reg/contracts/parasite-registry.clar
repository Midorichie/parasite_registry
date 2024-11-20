;; Parasite Data Registry Smart Contract
;; Initial Implementation
;; Contract name: parasite-registry

(define-data-var contract-owner principal tx-sender)

;; Data structure for parasite records
(define-map parasite-records
    { record-id: uint }
    {
        parasite-name: (string-utf8 100),
        classification: (string-utf8 50),
        location: (string-utf8 100),
        date-recorded: uint,
        researcher: principal,
        metadata-hash: (buff 32)
    }
)

;; Keep track of total records
(define-data-var total-records uint u0)

;; Error codes
(define-constant ERR-NOT-AUTHORIZED (err u100))
(define-constant ERR-INVALID-RECORD (err u101))

;; Add new parasite record
(define-public (add-parasite-record 
    (parasite-name (string-utf8 100))
    (classification (string-utf8 50))
    (location (string-utf8 100))
    (metadata-hash (buff 32)))
    (let
        ((new-id (+ (var-get total-records) u1)))
        (map-set parasite-records
            { record-id: new-id }
            {
                parasite-name: parasite-name,
                classification: classification,
                location: location,
                date-recorded: block-height,
                researcher: tx-sender,
                metadata-hash: metadata-hash
            }
        )
        (var-set total-records new-id)
        (ok new-id)
    )
)

;; Read parasite record
(define-read-only (get-parasite-record (record-id uint))
    (map-get? parasite-records { record-id: record-id })
)

;; Get total number of records
(define-read-only (get-total-records)
    (ok (var-get total-records))
)