class big_endian:
   def __new__(cls, Endian = None):
      if isinstance(Endian, int):
         return Endian.to_bytes((Endian.bit_length() + 7) >> 3, 'big', signed=False) if Endian != 0 else b'\x00'
      elif isinstance(Endian, bytes):        
         return int.from_bytes(Endian, 'big', signed=False)
      return None
   
if __name__ == '__main__':
   assert big_endian() is None
   assert big_endian(12345) == b'09'
   assert big_endian(b'09') == 12345