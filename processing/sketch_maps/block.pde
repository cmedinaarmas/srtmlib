class Block{
  String filename;
  int sz;                //blockSize
  float min=10000;
  float max=0;
  boolean isVoid = false;
  boolean debug = false;
  boolean releaseMemory = true;
  
  byte loadedData[];      //contains loaded data from file
  int  loadedHeigths[];  
  int  blockBuffer[];  

  //-----------------------------------------------------------------------
  Block(String[] path, int blockSize){                  //constructor
  
      String filenameWithExtention = path[1];          //extract filename for reference
      String[] splitted = split(filenameWithExtention,".");
      filename = splitted[0];
      
      String fullPath = join(path,"");                //build complete filepath
      print(fullPath);
      
      byte data[] = loadBytes(fullPath);              //try to load data
      
      if(data != null){
        loadedData = data;
        println(" "+data.length/1024+" KB"+" ->"+data.length+" values");
        isVoid = false;
      }
      else{
        isVoid = true;
        println("Void block");
        filename = "void";
     }
   sz = blockSize;
   
   if(releaseMemory) data= new byte[0];
   if(debug) println("Raw data file loaded "+loadedData.length+" values");
  }
  //-----------------------------------------------------------------------
  void byte2height(){
    if(debug) println("Converting data to heights");
    
    int[] heights = new int[sz*sz];                //convert selected heights and store in a buffer
    
    if(debug)println(loadedData.length+" loaded data length");
    if(debug)println(sz*sz+" height array size");
    
    int elements = 0;
    if(!isVoid){                                   //verify that the block is not void
       for(int i=0; i<loadedData.length-(2*(sz+1)); ){
          if((i==0)||(i % (2*(sz)) != 0)){
              
          int a = loadedData[i+1] & 0xff;           //high order byte
          a = a << 8;
          int a2 = loadedData[i] & 0xff;           //low order byte
          //a=0;  //uncomment to produce wrapped image
          
          int h = a + a2;

          if ( h < 0) h=0; //no data -32767
          else{
            if (h < min) min = h;
            if (( h>max )&&( h<8000 )) max = h;
          }
        
          heights[elements] = h; 
          i=i+2;
          elements++;
        }
        else{
          i=i+2;
        }
      }
    }
    else{                                      //if block is void
      for (int i = 0; i < sz*sz; i++)
        heights[i] = 0;
    }
   loadedHeigths = heights;
   println("Converted "+elements+" elements");
   if(debug) println("Converted "+loadedHeigths.length+" heights");
  
   if(releaseMemory){ 
         heights= new int[0];
         loadedData= new byte[0];
   }
  }
  //-----------------------------------------------------------------------
  void shadedRelief(){
    int minPixelval = 0;
    int maxPixelval = 255;
    int basePixelval = 128;
    int val = 0;
    int slope = 2;
    int slope_f = 5;
    
    int[] buffer = new int[sz*sz];
    //for(int i=0;i<buffer.length;i++)  buffer[i]=10000;
    
    if(!isVoid){                    //verify that the block is not void
    for (int i = 0; i < loadedHeigths.length; i++ ){
      if(i<loadedHeigths.length-sz){                        //avoid last row
        int delta = loadedHeigths[i] - loadedHeigths[i+sz];  //compare with pixel below

        if( (delta>0) && (delta>slope) ){         //ascending
         val = (int)(basePixelval+delta*slope_f);
         if(val>maxPixelval)  val=maxPixelval;  
         }
         
        else if( (delta<0) && (delta<-slope) ){   //descending
         val = (int)(basePixelval+delta*slope_f);
         if(val<minPixelval)  val=minPixelval;
         }
         
        else                                   //flat
        val = (int)basePixelval;
      }
      buffer[i]= val;
    }
    }
    else {
      for(int i=0;i<sz*sz;i++) 
        buffer[i]= 0;
    }
    
    blockBuffer = buffer;
  }
  //----------------------------------------------------------------------------
void rawHeights(int normalize){
    
    int[] buffer = new int[sz*sz];
    
    if(!isVoid){                    //verify that the block is not void
      for (int i = 0; i < loadedHeigths.length; i++ ){
        int val;
        if(normalize==0)  val = (int) loadedHeigths[i];
        else              val = (int) ( ( loadedHeigths[i] - min ) * 255 / (max - min) );                 //normalize values
        buffer[i]= val;
      }
    }
    else {
      for(int i=0;i<sz*sz;i++) 
        buffer[i]= 0;
    }
    
    blockBuffer = buffer;
    buffer = new int[0];      //release buffer memory
  }
  //-----------------------------------------------------------------------
  void saveBuffer2Image(){
    PImage img = createImage(sz, sz, RGB);
    img.loadPixels();  
    
    for(int i = 0; i < sz*sz; i++){
      int val = blockBuffer[i];
      img.pixels[i] = color(val, val, val);     //color each pixel
    }
      img.updatePixels();
      
      String[] path = new String[3];
      path[0]="b:/";
      path[1]=filename;
      path[2]=".png";
      
      String imagePath = join(path,"");
      img.save(imagePath);
      println(imagePath+" saved");
      
  }
  //-----------------------------------------------------------------------
  //-----------------------------------------------------------------------
  void printData(int[] data, int range, boolean top){
    if(top){
      for(int i=0;i<range;i++)
        print(data[i]+"\t");
        println();
    }
    else{ 
      for(int i=data.length-range;i<data.length;i++)
        print(data[i]+"\t");
        println(); 
    }
  }
  //-----------------------------------------------------------------------
  void printData(byte[] data, int range, boolean top){
    if(top){
      for(int i=0;i<2*range;){
        print(i+":"+data[i]+"  "+data[i+1]+"\t");
        i=i+2;
      }
    }
    else{ 
      for(int i=data.length-(2*range);i<data.length;){
        print(i+":"+data[i]+" "+data[i+1]+"\t");
        i=i+2;
      } 
    }
    println(); 
  }
  //-----------------------------------------------------------------------
  void printLoadedHeights(int numElements,boolean top){
    println(loadedHeigths.length + " Heights");
    printData(loadedHeigths, numElements, top);
  }
  //-----------------------------------------------------------------------
  void printLoadedData(int numElements,boolean top){
    print(loadedData.length + " Bytes"+" ");
    printFilename();
    
    printData(loadedData, numElements, top);
  }
  //-----------------------------------------------------------------------
  void printFilename(){
    if(!isVoid) println(filename);
    else  println("Void file");
  }
  //-----------------------------------------------------------------------
  void freeLoadedHeighs(){
    loadedHeigths = new int[0];
  }
  
}
//-----------------------------------------------------------------------