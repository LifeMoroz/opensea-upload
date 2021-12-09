import json
import os
import time

import dotenv

from uploader import Uploader


def main():
    # Initialize env variables
    dotenv.load_dotenv()
    seed_phrase = os.getenv("SEED_PHRASE")
    password = os.getenv("PASSWORD")

    # Initialize
    uploader = Uploader()
    uploader.connect_metamask(seed_phrase, password)

    # Connect to the specified network - ENTER THE APPROPRIATE NETWORK
    NETWORK_RPC = "https://polygon-mainnet.g.alchemy.com/v2/nV3XqnDJF7y7bmXTQhrJB13lcK1aAAWF"
    CHAIN_ID = 137
    uploader.set_network(NETWORK_RPC, CHAIN_ID)  # Custom network to add to Metamask
    uploader.open_metamask()

    # Connect to OpenSea
    uploader.connect_opensea(False)
    COLLECTION_URL = "https://opensea.io/collection/mewmodernsimplecollection"
    uploader.set_collection_url(COLLECTION_URL)

    # Upload NFT data in 'metadata.json' to OpenSea - MODIFY THE UPLOAD FUNCTION AND THE METADATA TO CONTAIN ANY ADDITIONAL METADATA
    metadata = json.load(open(os.path.join(os.getcwd(), "data", "metadata.json")))
    first_upload = True
    for i, data in enumerate(metadata):
        uploader.upload(data)
        if first_upload:
            uploader.sign_transaction()
            first_upload = False
        time.sleep(2)
        uploader.sell()
        time.sleep(1)
    # Close
    uploader.close()


# Run main if this file is run directly
if __name__ == "__main__":
    main()
