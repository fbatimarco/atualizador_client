# Checa se a maquina eh uma raspberry PI
def getModel():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'Raspberry' in line:
                    return 'arm'
    except:
        pass
    
    return 'x86'

# Pegamos o modelo da maquina
modelo_processador = getModel()
print(str(modelo_processador))
