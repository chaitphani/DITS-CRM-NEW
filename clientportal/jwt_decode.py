import jwt

# outgoing_secret_key = "9FNe7xDnaPnYDkm62nBJ"
# incoming_secret_key = "LcTCqAjmQtF58cEce7R3"
outgoing_secret_key = "6JJ4Mnm7G9aEWfUksRy5"
incoming_secret_key = "U3A9qNdz6MxVtBvPv3Lj"

def encode_jwt(outgoing_key=outgoing_secret_key, data=None):
    decoded_value = jwt.encode(data, outgoing_key, algorithm='HS256').decode()
    print(decoded_value)
    return decoded_value


# account_open
dict_data = {
  "comp_id": "X!n|U@N!2",
  "comp_pass": "6LCWP53LPwJhtPNyKYtU",
  "leverage": "200",
  "company": "HANMENGHUI",
  "enable": "1",
  "readonly": "0",
  "account_type": "TStandard"
}

dict_data_premium = {
  "comp_id": "X!n|U@N!2",
  "comp_pass": "6LCWP53LPwJhtPNyKYtU",
  "leverage": "200",
  "company": "HANMENGHUI",
  "enable": "1",
  "readonly": "0",
  "account_type": "Premium",
#   "group":"A_XN_VIP2_USD"
}

dict_data_supreme = {
  "comp_id": "X!n|U@N!2",
  "comp_pass": "6LCWP53LPwJhtPNyKYtU",
  "leverage": "200",
  "company": "HANMENGHUI",
  "enable": "1",
  "readonly": "0",
  "account_type": "Supreme"
}

dict_data_vip = {
  "comp_id": "X!n|U@N!2",
  "comp_pass": "6LCWP53LPwJhtPNyKYtU",
  "leverage": "200",
  "company": "HANMENGHUI",
  "enable": "1",
  "readonly": "0",
  "account_type": "VIP"
}

dict_data_demo = {
  "comp_id": "X!n|U@N!2",
  "comp_pass": "6LCWP53LPwJhtPNyKYtU",
  "leverage": "200",
  "company": "HANMENGHUI",
  "enable": "1",
  "readonly": "0",
  "account_type": "Standard"
}

# pls open the view for this
account_get_data = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Real",
}

withdraw_data = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
}

deposit_data = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Real",
}

edit_account = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Real",
    # "currency": "USD",
#    "leverage": "1000",
#    "company": "HNXINLUAN",
    # "id": "test",
    # "country": "india",
#    "enable": "1",
#    "readonly": "0",
    # "client_name": "Sandip",
    # "client_email": "sandy@gmail.com",
    # "client_ip": "127.0.0.1",
    # "server": "Demo",
#    "account_type": "Standard"
}

live_account_data = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Real"
}

demo_account_data = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Demo"
}

reset_account_pwd = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Real"
}

investor_password_pwd = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Real"
}

check_password_dict = {
    "comp_id": "X!n|U@N!2",
    "comp_pass": "6LCWP53LPwJhtPNyKYtU",
    "server": "Real"
}

# print(encode_jwt(outgoing_secret_key, dict_data))

## post encode_jwt data to API url using 'request_message=ENCODED_DATA'

def decode_jwt(incoming_key=incoming_secret_key, data=None):
    decoded_value = jwt.decode(data, incoming_key, algorithms=['HS256'], verify=False)
    print(decoded_value)
    return decoded_value


# print(decode_jwt(incoming_secret_key, response_data))
