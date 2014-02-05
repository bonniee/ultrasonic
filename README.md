# An Ultrasonic Encoder/Decoder for Python

## Wait, why?

This project was produced by Bonnie Eisenman and Harvest Zhang for our final project in a graduate seminar, COS 597G: Surveillance and Countermeasures.

## What's here?

The repo contains three files of interest:

- sound_encoder.py: For encoding stuff.
- sound_decoder.py: For decoding stuff.
- squeakychat.py: For testing and demonstration.

## Abstract
We explored the feasibility of using ultrasonic communication as a covert channel in consumer electronics products. We describe the implementation of an ultrasonic encoder and decoder, as well as a prototype chat client (“SqueakyChat”) used to demonstrate this functionality. We were able to sustain a transmission rate of 1 byte per second for arbitrary binary data, and we obtained up to 99.5% accuracy when broadcasting across 0 feet, and up to 81.6% accuracy when broadcasting across 10 feet. While this throughput is still quite low, we have demonstrated that for small messages ultrasonic communication is quite feasible using standard microphones and speakers shipped in consumer electronics. We then discuss limitations of this type of communication as well as potential use cases.

## Report

Available in the repo; see SqueakyChat.pdf.
