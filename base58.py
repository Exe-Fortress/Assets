class base58:
   def __init__(self, Base58 = None):
      self.Base58 = Base58
      self.CHAR = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

   def encode(self) -> bytes:
      if isinstance(self.Base58, (str, bytes)):
         if isinstance(self.Base58, str): 
            self.Base58 = self.Base58.encode()
         num = big_endian(self.Base58) # used big_endian
         result = [self.CHAR[0]] * (len(self.Base58) - len(self.Base58.lstrip(b'\x00')))
         while num > 0: 
            num, rmd = divmod(num, 58)
            result.append(self.CHAR[rmd].encode())
         return b''.join(result[::-1])
      return None

   def decode(self) -> bytes:
      if isinstance(self.Base58, (str, bytes)):      
         if len(self.Base58) > 0:    
            if isinstance(self.Base58, bytes): 
               self.Base58 = self.Base58.decode(); 
            num = 0
            for Char in self.Base58.rstrip(self.CHAR[0]): 
               num = num * 58 + self.CHAR.index(Char)
            return (b'\x00' * (len(self.Base58) - len(self.Base58.lstrip(self.CHAR[0])))) + big_endian(num) # used big_endian
         return b'' 
      return None

   def encode_check(self) -> bytes:
      if isinstance(self.Base58, (str, bytes)):
         if isinstance(self.Base58, str): 
            self.Base58 = self.Base58.encode()
         result = [self.CHAR[0]] * (len(self.Base58) - len(self.Base58.lstrip(b'\x00')))
         self.Base58 += sha256(sha256(self.Base58).digest()).digest()[:4] # used sha256
         num = big_endian(self.Base58) # used big_endian
         while num > 0:
            num, rmd = divmod(num, 58)
            result.append(self.CHAR[rmd].encode())
         return b''.join(result[::-1])
      return None

   def decode_check(self) -> bytes:
      if isinstance(self.Base58, (str, bytes)):
         if isinstance(self.Base58, bytes):
            self.Base58 = self.Base58.decode()
         num = sum(self.CHAR.index(Char) * (58 ** i) for i, Char in enumerate(self.Base58[::-1]))
         data = big_endian(num) # used big_endian
         checksum = data[-4:]
         data = data[:-4]
         if checksum == sha256(sha256(data).digest()).digest()[:4]: # used sha256
            return (b'\x00' * (len(self.Base58) - len(self.Base58.lstrip(self.CHAR[0])))) + data
      return None
   
if __name__ == '__main__':
   var = b'Hello, World'
   assert base58().encode() is None
   assert base58(var).encode() is not None
   assert base58(var).encode() == b'2NEpo7TZsLBYdvo5V'

   assert base58().decode() is None
   assert base58(b'2NEpo7TZsLBYdvo5V').decode() is not None
   assert base58(b'2NEpo7TZsLBYdvo5V').decode() == var

   assert base58().encode_check() is None
   assert base58(var).encode_check() is not None
   assert base58(var).encode_check() == b'9wWTEnNWQV2M4vYkWHTqLQ'

   assert base58().decode_check() is None
   assert base58(b'9wWTEnNWQV2M4vYkWHTqLQ').decode_check() is not None
   assert base58(b'9wWTEnNWQV2M4vYkWHTqLQ').decode_check() == var