# EQE Measurement 

This repository was built to employ a monochromater, optical power meter, and multimeter to measure the external quantum efficiency of solar cell samples in Professor Mool Gupta's lab in the Electrical Engineering department of the University of Virginia.

The instrument interfaces (MonoChromater.py, PowerMeter.py, and SourceMeter.py) are built using pyVisa commands to interface with their respective instruments. 

The EQEMeasurement.py module runs the EQE scan, gathering readings from each of the devices. Measured power and current values are temporarily stored in arrays, and data isn't recorded until the standard deviation of these values dips under 3 percent. This uncertainty
 gate is intended to counteract some of the inherent variability in this setup, which arises from unavoidable circumstances such as the variability of the xenon lamp source, the charateristic drifting of thermopile optical meters, and ambient nose in the room.
 
 As you scan the sample, the tqdm module will give you an estimation of the time remaining. It's based on how long it took to get a dataset with a pretty low stdev at the lower end of the spectrum where you started, 
 but if you've isolated your setup well, then it should be pretty accurate. Shoutout to those people for making a great little plugin. 
 
 Direct any questions about the repository to me, Rex Serpe, at 757-335-1886, or rjs4my@virginia.edu if I don't pick up my phone. 
 
 If you're working in Professor Gupta's lab and any of the instruments are giving you issues, check the cables. Damn those cables. 