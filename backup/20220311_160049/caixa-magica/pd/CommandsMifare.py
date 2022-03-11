import logging

class CommandsMifare():
        
    def __init__(self):
        pass
    
    def command_select_card(self):
        # logging.info("Command Select Card")        
        command = [0]*4
        command[0] = 0xBA
        command[1] = 0x02
        command[2] = 0x01 #Command Select Card
        cs = command[0] ^ command[1] ^ command[2] #XOR entre os dados para criar CHECKSUM
        command[3] =  cs
        # logging.warning("Command select card ready: " + str(command))
        return command
    
    def command_store_key(self,key_type, key_number, key):
        # logging.info("Command Store Key")        
        command = [0]*12
        command[0] = 0xBA
        command[1] = 0x0A
        command[2] = 0x13 #Command Store key
        command[3] = key_number
        command[4] = int(key[0],16)
        command[5] = int(key[1],16)
        command[6] = int(key[2],16)
        command[7] = int(key[3],16)
        command[8] = int(key[4],16)
        command[9] = int(key[5],16)
        command[10] = key_type
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] ^ command[10]  
        command[11] = cs
        # logging.warning("Command store key ready: " + str(command))
        return command


    def command_login(self, sector, key_type, key):
        # logging.info("Command Store Key")        
        command = [0]*12
        command[0] = 0xBA
        command[1] = 0x0A
        command[2] = 0x0E #Command Store key
        command[3] = sector
        command[4] = key_type
        command[5] = key[0]
        command[6] = key[1]
        command[7] = key[2]
        command[8] = key[3]
        command[9] = key[4]
        command[10] = key[5]
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] ^ command[10]  
        command[11] =  cs
        # logging.warning("Command store key ready: " + str(command))
        return command



    def command_login_sector(self, sector, key_type, key):
        # logging.info("Command Store Key")        
        command = [0]*12
        command[0] = 0xBA
        command[1] = 0x0A
        command[2] = 0x02 #Command Login to Sector
        command[3] = sector
        command[4] = key_type
        command[5] = key[0]
        command[6] = key[1]
        command[7] = key[2]
        command[8] = key[3]
        command[9] = key[4]
        command[10] = key[5]
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] ^ command[10]  
        command[11] =  cs
        # logging.warning("Command store key ready: " + str(command))
        return command


    def command_write_master_key_a(self, sector, key):
        logging.info("Command Write Master Key A")        
        command = [0]*11
        command[0] = 0xBA
        command[1] = 0x09
        command[2] = 0x07 #Command write master key A
        command[3] = sector
        command[4] = int(key[0],16)
        command[5] = int(key[1],16)
        command[6] = int(key[2],16)
        command[7] = int(key[3],16)
        command[8] = int(key[4],16)
        command[9] = int(key[5],16)
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] 
        command[10] =  cs
        # logging.warning("Command ready: " + str(command))
        return command


    def command_write_keys(self, sector, key):
        logging.info("Command Write Block")        
        command = [0]*21
        command[0] = 0xBA
        command[1] = 0x13
        command[2] = 0x04 #Command Write Block
        command[3] = (sector*4) + 0x03 #Block 3 keep Keys
        command[4] = int(key[0],16)
        command[5] = int(key[1],16)
        command[6] = int(key[2],16)
        command[7] = int(key[3],16)
        command[8] = int(key[4],16)
        command[9] = int(key[5],16)
        command[10] = 0xFF
        command[11] = 0x07
        command[12] = 0x80
        command[13] = 0x69
        command[14] = int(key[0],16)
        command[15] = int(key[1],16)
        command[16] = int(key[2],16)
        command[17] = int(key[3],16)
        command[18] = int(key[4],16)
        command[19] = int(key[5],16)               
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] ^ command[10]  ^ command[11] ^ command[12] ^ command[13] ^ command[14] ^ command[15] ^ command[16] ^ command[17] ^ command[18] ^ command[19]
        command[20] =  cs
        # logging.warning("Command Write Block ready: " + str(command))
        return command

    
    def command_write_data_info(self, cpf, card):
        logging.info("Command Write Data Info")        
        command = [0]*21
        command[0] = 0xBA
        command[1] = 0x13
        command[2] = 0x04 #Command Write Block
        command[3] = 0x04 #Setor 1 e Bloco 0
        command[4] = int(card[5],16)
        command[5] = cpf[0]
        command[6] = cpf[1]
        command[7] = cpf[2]
        command[8] = cpf[3]
        command[9] = cpf[4]
        command[10] = cpf[5]
        command[11] = cpf[6]
        command[12] = cpf[7]
        command[13] = cpf[8]
        command[14] = cpf[9]
        command[15] = cpf[10]
        command[16] = int(card[4],16)
        command[17] = int(card[3],16)
        command[18] = int(card[2],16)
        command[19] = int(card[1],16)                
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] ^ command[10]  ^ command[11] ^ command[12] ^ command[13] ^ command[14] ^ command[15] ^ command[16] ^ command[17] ^ command[18] ^ command[19]
        command[20] =  cs
        # logging.warning("Command Write Data Info Ready: " + str(command))
        return command
    
    
    def command_write_info_credit(self, cpf, card, real, centavos, linha):
        logging.info("Command Write Info Credit")        
        command = [0]*21
        command[0] = 0xBA
        command[1] = 0x13
        command[2] = 0x04 #Command Write Block
        command[3] = 0x05 #Setor 1 e bloco 1
        command[4] = int(card[1],16)
        command[5] = int(card[0],16)
        command[6] = cpf[0]
        command[7] = cpf[1]
        command[8] = cpf[2]
        command[9] = cpf[3]
        command[10] = real[3]
        command[11] = real[2]
        command[12] = real[1]
        command[13] = real[0]
        command[14] = centavos[1]
        command[15] = centavos[0]
        command[16] = linha[0]
        command[17] = linha[1]
        command[18] = linha[2]
        command[19] = linha[3]                
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] ^ command[10]  ^ command[11] ^ command[12] ^ command[13] ^ command[14] ^ command[15] ^ command[16] ^ command[17] ^ command[18] ^ command[19]
        command[20] =  cs
        # logging.warning("Command Write Data Info Ready: " + str(command))
        return command


    def command_write_data_hora_log(self, data_hora):
        #logging.info("Command Write Info Credit")        
        command = [0]*21
        command[0] = 0xBA
        command[1] = 0x13
        command[2] = 0x04 #Command Write Block
        command[3] = 0x06 #Setor 1 e bloco 2
        command[4] = data_hora[0]  #D1
        command[5] = data_hora[1]  #D2
        command[6] = data_hora[2]  #m1
        command[7] = data_hora[3]  #m2
        command[8] = data_hora[4]  #A1
        command[9] = data_hora[5]  #A2
        command[10] = data_hora[6] #A3
        command[11] = data_hora[7] #A4
        command[12] = data_hora[8] #H1
        command[13] = data_hora[9] #H2
        command[14] = data_hora[10]#M1
        command[15] = data_hora[11]#M2
        command[16] = data_hora[12]#S1
        command[17] = data_hora[13]#S2
        command[18] = 0x00 #R1
        command[19] = 0x00 #R2                
        #XOR entre os dados para criar CHECKSUM
        cs = command[0] ^ command[1] ^ command[2] ^ command[3] ^ command[4] ^ command[5] ^ command[6] ^ command[7] ^ command[8] ^ command[9] ^ command[10]  ^ command[11] ^ command[12] ^ command[13] ^ command[14] ^ command[15] ^ command[16] ^ command[17] ^ command[18] ^ command[19]
        command[20] =  cs
        # logging.warning("Command Write Data Info Ready: " + str(command))
        return command
    
    
    def command_read_data_info(self):
        # logging.info("Command Read Sector 1  Block 0")        
        command = [0]*5
        command[0] = 0xBA
        command[1] = 0x03
        command[2] = 0x03 
        command[3] = 0x04 #Setor 1 e Bloco 0
        cs = command[0] ^ command[1] ^ command[2] ^ command[3]#XOR entre os dados para criar CHECKSUM
        command[4] =  cs
        # logging.warning("Command read sector ready: " + str(command))
        return command    
    

    def command_read_info_credit(self):
        # logging.info("Command Read Sector 1  Block 1")        
        command = [0]*5
        command[0] = 0xBA
        command[1] = 0x03
        command[2] = 0x03 
        command[3] = 0x05 #Setor 1 e Bloco 1
        cs = command[0] ^ command[1] ^ command[2] ^ command[3]#XOR entre os dados para criar CHECKSUM
        command[4] =  cs
        # logging.warning("Command read sector ready: " + str(command))
        return command

    def get_keys_predefined(self):
        #KEY DEFAULT
        key_def = [0]*6    
        key_def[0] = 0xFF
        key_def[1] = 0xFF
        key_def[2] = 0xFF
        key_def[3] = 0xFF
        key_def[4] = 0xFF
        key_def[5] = 0xFF

        #KEY 0
        key_0 = [0]*6    
        key_0[0] = 0xDE
        key_0[1] = 0x45
        key_0[2] = 0xAB
        key_0[3] = 0x1A
        key_0[4] = 0x90
        key_0[5] = 0x50

        #KEY 1
        key_1 = [0]*6    
        key_1[0] = 0xDD
        key_1[1] = 0x49
        key_1[2] = 0xAB
        key_1[3] = 0x4A
        key_1[4] = 0x93
        key_1[5] = 0x5A

        #KEY 2
        key_2 = [0]*6    
        key_2[0] = 0xD0
        key_2[1] = 0x45
        key_2[2] = 0x99
        key_2[3] = 0x1D
        key_2[4] = 0xD0
        key_2[5] = 0x5C

        #KEY 3
        key_3 = [0]*6    
        key_3[0] = 0x99
        key_3[1] = 0x45
        key_3[2] = 0x00
        key_3[3] = 0x13
        key_3[4] = 0x40
        key_3[5] = 0x5C

        #KEY 4
        key_4 = [0]*6    
        key_4[0] = 0x88
        key_4[1] = 0x45
        key_4[2] = 0xD4
        key_4[3] = 0x19
        key_4[4] = 0xB0
        key_4[5] = 0x5C

        #KEY 5
        key_5 = [0]*6    
        key_5[0] = 0xDE
        key_5[1] = 0x44
        key_5[2] = 0xAB
        key_5[3] = 0xAB
        key_5[4] = 0x90
        key_5[5] = 0x89

        #KEY 6
        key_6 = [0]*6    
        key_6[0] = 0x88
        key_6[1] = 0x48
        key_6[2] = 0x8B
        key_6[3] = 0x55
        key_6[4] = 0x90
        key_6[5] = 0xAC

        #KEY 7
        key_7 = [0]*6    
        key_7[0] = 0x90
        key_7[1] = 0x42
        key_7[2] = 0x1B
        key_7[3] = 0x1A
        key_7[4] = 0xFF
        key_7[5] = 0x51

        #KEY 8
        key_8 = [0]*6    
        key_8[0] = 0xD2
        key_8[1] = 0x43
        key_8[2] = 0x3B
        key_8[3] = 0x44
        key_8[4] = 0x98
        key_8[5] = 0xFC        

        #KEY 9
        key_9 = [0]*6    
        key_9[0] = 0xDE
        key_9[1] = 0x43
        key_9[2] = 0x3B
        key_9[3] = 0x11
        key_9[4] = 0x10
        key_9[5] = 0x97

        #KEY 10
        key_10 = [0]*6    
        key_10[0] = 0xD6
        key_10[1] = 0x4D
        key_10[2] = 0xDB
        key_10[3] = 0xDD
        key_10[4] = 0x9C
        key_10[5] = 0x97
            
        #KEY 11
        key_11 = [0]*6    
        key_11[0] = 0x43
        key_11[1] = 0x45
        key_11[2] = 0xD5
        key_11[3] = 0x1F
        key_11[4] = 0xF0
        key_11[5] = 0x5B

        #KEY 12
        key_12 = [0]*6    
        key_12[0] = 0x87
        key_12[1] = 0x45
        key_12[2] = 0xAD
        key_12[3] = 0xDA
        key_12[4] = 0xAA
        key_12[5] = 0x5C
         
        #KEY 13
        key_13 = [0]*6    
        key_13[0] = 0xD9
        key_13[1] = 0x33
        key_13[2] = 0xA5
        key_13[3] = 0x5A
        key_13[4] = 0xDF
        key_13[5] = 0x52

        #KEY 14
        key_14 = [0]*6    
        key_14[0] = 0xDA
        key_14[1] = 0x45
        key_14[2] = 0x22
        key_14[3] = 0x16
        key_14[4] = 0x80
        key_14[5] = 0x5C

        #KEY 15
        key_15 = [0]*6    
        key_15[0] = 0x99
        key_15[1] = 0x45
        key_15[2] = 0x4B
        key_15[3] = 0x1F
        key_15[4] = 0x0E
        key_15[5] = 0x50


        list_keys = [0]*17
        list_keys[0] = key_def
        list_keys[1] = key_0
        list_keys[2] = key_1
        list_keys[3] = key_2
        list_keys[4] = key_3
        list_keys[5] = key_4
        list_keys[6] = key_5
        list_keys[7] = key_6
        list_keys[8] = key_7
        list_keys[9] = key_8
        list_keys[10] = key_9
        list_keys[11] = key_10
        list_keys[12] = key_11
        list_keys[13] = key_12
        list_keys[14] = key_13
        list_keys[15] = key_14
        list_keys[16] = key_15
        
        return list_keys
