from numpy import log, exp

def client_to_ui_vol(vol):
    if (vol <= 0):
        return 0
    elif (vol <= 100):
        return 17.362 * log(vol) + 20.054
    else :
        return 144.86 * log(vol) - 567.21

def ui_to_client_vol(vol):
    if (vol <= 0):
        return 0
    elif (vol <= 100):
        return exp((vol - 20.054) / 17.362)
    else :
        return exp((vol + 567.21) / 144.86)