# sCAN
This is a python script that parses the data of 2 CSV files, that were created using combination of CAN(controller area network) 
capture hardware and software. The script generates an output file, producing information showing how many times each hex value appears,
the hex values locations inside the IDs, and the frequency of changes in values between the two CSVs. This CAN data was produced by my motorcycle's ECM(Engine Control Module). The purpose of these CAN capture sessions, and the script used to analyze them, is to reverse engineer the ECM and CAN definitions, so that I can design after market parts and software to interface with the ECM.

The hardware used is the Seeedstudio USB-CAN Analyzer SKU 114991193

The software is found here https://github.com/SeeedDocument/USB-CAN-Analyzer

The following is an example of what the first row in the CSV should resemble. Out of the 15 occupied collumns, the program uses 9 of them for parsing data. The Frame_ID and the 8 byte collumns(ByteA,ByteB,ByteC,ByteD,ByteE,ByteF,ByteG,ByteH).

No,Direction,Time_Scale,Frame_Type,Frame_Format,Frame_ID,Data_Length,ByteA,ByteB,ByteC,ByteD,ByteE,ByteF,ByteG,ByteH
