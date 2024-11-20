# Blockchain-Based Parasite Data Registry 🦠

A decentralized platform for storing and managing global parasitology data using blockchain technology. This project ensures transparency, traceability, and immutability of parasitological research data while facilitating global collaboration among researchers and institutions.

## 🌟 Features

- **Immutable Data Storage**: Secure storage of parasite records on the Stacks blockchain
- **Version Control**: Track changes and updates to parasite records over time
- **Institution Verification**: Verified research institutions system
- **Geographic Tracking**: Statistical analysis of parasite distribution
- **IPFS Integration**: Distributed storage for additional research files
- **Data Validation**: Comprehensive validation system for data integrity
- **Access Control**: Role-based permissions for researchers and institutions

## 🛠️ Technology Stack

- **Smart Contracts**: Clarity (Stacks Blockchain)
- **Backend**: Python 3.8+
- **Blockchain**: Stacks Network
- **File Storage**: IPFS
- **Data Analysis**: Pandas

## 📋 Prerequisites

- Python 3.8 or higher
- Stacks CLI
- Node.js and NPM (for contract deployment)
- Access to Stacks network (Mainnet or Testnet)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/parasite-registry.git
cd parasite-registry
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 📖 Usage

### Smart Contract Deployment

1. Deploy the contract to Stacks network:
```bash
stx deploy parasite-registry.clar
```

### Python Pipeline

1. Initialize the pipeline:
```python
from parasite_pipeline import ParasiteDataPipeline

pipeline = ParasiteDataPipeline(
    stacks_api_url="https://stacks-node-api.mainnet.stacks.co",
    ipfs_gateway="https://ipfs.io"
)
```

2. Create and submit a parasite record:
```python
record = ParasiteRecord(
    parasite_name="Plasmodium falciparum",
    classification="Apicomplexan",
    location="Sub-Saharan Africa",
    metadata={
        "resistance_profile": "chloroquine-resistant",
        "prevalence": "high"
    },
    researcher="DR_SMITH",
    institution="WHO_AFRICA"
)

prepared_data = await pipeline.prepare_parasite_data(record)
result = await pipeline.submit_to_blockchain(prepared_data)
```

## 🏗️ Project Structure

```
parasite-registry/
├── contracts/
│   ├── parasite-registry.clar      # Main smart contract
│   └── parasite-registry-v2.clar   # Enhanced version
├── src/
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── data_processor.py
│   │   └── blockchain_interface.py
│   └── utils/
│       ├── validation.py
│       └── ipfs_handler.py
├── tests/
│   ├── test_contract.py
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```

## 🔍 Smart Contract Functions

### Main Functions

- `add-parasite-record`: Add new parasite data
- `update-parasite-record`: Update existing records
- `register-institution`: Register research institutions
- `verify-institution`: Verify research institutions
- `get-parasite-record-history`: Get record version history
- `get-geographic-stats`: Get geographical statistics

## 📊 Data Pipeline Features

- Asynchronous data processing
- Retry mechanism for resilient operations
- IPFS integration for large file storage
- Comprehensive data validation
- Geographic distribution analysis
- Record version history tracking

## 🔐 Security

- Institution verification system
- Role-based access control
- Data integrity validation
- Immutable record tracking
- Version control for all updates

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Stacks Blockchain team
- IPFS development team
- Global parasitology research community

## 📧 Contact

Project Maintainer - [your-email@example.com](mailto:your-email@example.com)

Project Link: [https://github.com/yourusername/parasite-registry](https://github.com/yourusername/parasite-registry)

## 🔄 Version History

- 2.0.0
  - Added institution verification
  - Implemented version control
  - Added geographic tracking
  - Enhanced security features
- 1.0.0
  - Initial Release
  - Basic parasite data storage
  - Simple validation system