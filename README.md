# Nano Block Validator

## Overview
The **Nano Block Validator** is a comprehensive tool designed to validate Nano cryptocurrency blocks. 
This application offers a user-friendly interface to validate the authenticity and integrity of Nano blocks by performing signature checking and proof of work (PoW) verification. 
It supports both live and beta networks and accommodates various block types, ensuring broad applicability and utility.

## Features
- **Signature Verification:** Validates the digital signature of a block to confirm its authenticity. This step ensures that the block was indeed created by the holder of the private key and has not been tampered with.
- **Proof of Work Verification:** Checks the proof of work for both live and beta networks to confirm that the necessary computational effort has been expended. This feature supports different thresholds depending on the network (live or beta) and the type of block (send, receive, change), offering tailored validation.
- **Support for Various Block Types:** Whether dealing with send, receive, or change blocks, the Nano Block Validator is equipped to handle and accurately validate them.

## How to Use
Visit `https://verifyblock.bnano.info`
1. **Prepare the Block:** The application requires block information in JSON format. Ensure your block data is structured correctly, following the Nano block specifications.
2. **Copy and Paste the Block:** Navigate to the text field on the application's interface. Copy your block in JSON format and paste it into the multiline text field provided.
3. **Validate the Block:** Once your block is entered, click on the "Validate" button. The application will then process the block, verifying both the signature and the proof of work based on the selected network type (live or beta).

## Example Block Format
```json
{
    "type": "open",
    "source": "E89208DD038FBB269987689621D52292AE9C35941A7484756ECCED92A65093BA",
    "representative": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
    "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
    "work": "62f05417dd3fb691",
    "signature": "9F0C933C8ADE004D808EA1985FA746A7E95BA2A38F867640F53EC8F180BDFE9E2C1268DEAD7C2664F356E37ABA362BC58E46DBA03E523A7B5A19E4B6EB12BB02"
}
```
## Self hosting
```
docker-compose build && docker-compose up -d
```
Visit `http://localhost:5015`



