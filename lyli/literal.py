
def split_int(str):
  prefix = None
  body = None
  suffix = None
  if str[:2] in ["0b","0o","0d","0x"]:
    prefix = str[:2]
    str = str[2:]
  if str[-2:] in ["i8","u8"]:
    suffix = str[-2:]
    body = str[:-2]
  elif str[-3:] in ["i16","i32","i64","u16","u32","u64"]:
    suffix = str[-3:]
    body = str[:-3]
  else:
    body = str
  return (prefix, body, suffix)

def get_int_base(str):
  (prefix,body,suffix) = split_int(str)
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

def get_int_type(str):
  suffix = split_int(str)[2]
  return suffix if suffix else ""

def split_float(str):
  body = None
  suffix = None
  if str[-3:] in ["f32","f64"]:
    suffix = str[-3:]
    body = str[:-3]
  else:
    body = str
  return (body, suffix)

def get_float(str):
  body = split_float(str)[0]
  return float(body)

def get_float_type(str):
  suffix = split_float(str)[1]
  return suffix if suffix else ""
