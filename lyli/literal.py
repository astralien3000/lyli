
def split_int(str):
  prefix = None
  body = str
  if str[:2] in ["0b","0o","0d","0x"]:
    prefix = str[:2]
    body = str[2:]
  return (prefix, body)

def get_int_base(str):
  prefix = split_int(str)[0]
  convert = {
    None : 10,
    "0b" : 2,
    "0o" : 8,
    "0d" : 10,
    "0x" : 16,
  }
  return convert[prefix]

def get_int(str):
  base = get_int_base(str)
  body = split_int(str)[1]
  return int(body, base)
