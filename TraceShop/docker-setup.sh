docker build -t store:0.0.1 -f dockerfile.store .
docker build -t payments:0.0.1 -f dockerfile.payments .
docker build -t orders:0.0.1 -f dockerfile.orders .
