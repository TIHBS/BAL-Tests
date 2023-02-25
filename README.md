# BAL-Tests

This repository contains tests for BAL plugins

## Pre-requisites

- Run BAL gateway (port: 9091)
- Run Bal Callback handler (port: 5010)
- Run blockchain nodes as required: Aptos/Flow/Sui
- Run remote plugin in case of Flow and Sui

## Setup

```commandline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
pip install starkbank-ecdsa
```

### Running case study

#### Client 1

```commandline
python -m unittest tests.case_study.flow.test_client_1.TestClient1.test_initiate_invocation
```

#### Client 2

```commandline
python -m unittest tests.case_study.flow.test_client_1.TestClient2.test_sign_invocation
```