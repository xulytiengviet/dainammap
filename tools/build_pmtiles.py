"""Build a PMTiles v3 raster archive in pixel space (NOT georeferenced)."""
from PIL import Image
from pathlib import Path
import io,gzip,json,struct,sys
def varint(i):
 b=bytearray()
 while i>=128:b.append((i&127)|128);i>>=7
 b.append(i);return bytes(b)
def rot(n,x,y,rx,ry):
 if ry==0:
  if rx:x=n-1-x;y=n-1-y
  x,y=y,x
 return x,y
def tileid(z,x,y):
 v=((1<<(z*2))-1)//3
 for a in range(z-1,-1,-1):
  s=1<<a;rx=int(bool(x&s));ry=int(bool(y&s))
  v+=s*s*((3*rx)^ry);x,y=rot(s,x,y,rx,ry)
 return v
def main(src,dest):
 im=Image.open(src).convert('RGB');w,h=im.size
 side=max(w,h);maxz=4 if side>2048 else 3
 canvas=Image.new('RGB',(side,side),'white');canvas.paste(im,((side-w)//2,(side-h)//2))
 tiles=[]
 for z in range(maxz+1):
  n=1<<z;plane=canvas.resize((n*256,n*256),Image.Resampling.LANCZOS)
  for y in range(n):
   for x in range(n):
    buf=io.BytesIO();plane.crop((x*256,y*256,(x+1)*256,(y+1)*256)).save(buf,'JPEG',quality=88,optimize=True)
    tiles.append((tileid(z,x,y),buf.getvalue()))
 tiles.sort();directory=bytearray(varint(len(tiles)));last=0
 for tid,_ in tiles:directory+=varint(tid-last);last=tid
 for _ in tiles:directory+=varint(1)
 for _,data in tiles:directory+=varint(len(data))
 for i,(_,data) in enumerate(tiles):directory+=varint(1 if i==0 else 0)
 root=gzip.compress(bytes(directory),mtime=0)
 meta=gzip.compress(json.dumps({'name':'Dai Nam — image dated 1838','format':'jpg','image_width':w,'image_height':h,'coordinate_system':'CRS.Simple — NOT georeferenced'}).encode(),mtime=0)
 header=bytearray(b'PMTiles\x03')
 offsets=[127,len(root),127+len(root),len(meta),0,0,127+len(root)+len(meta),sum(len(d) for _,d in tiles),len(tiles),len(tiles),len(tiles)]
 for v in offsets:header+=struct.pack('<Q',v)
 header+=bytes([1,2,1,3,0,maxz])
 for v in [-1800000000,-850000000,1800000000,850000000]:header+=struct.pack('<i',v)
 header+=bytes([0])+struct.pack('<ii',0,0)
 assert len(header)==127
 Path(dest).parent.mkdir(parents=True,exist_ok=True)
 Path(dest).write_bytes(header+root+meta+b''.join(d for _,d in tiles))
 print('Created',dest,'tiles',len(tiles))
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
