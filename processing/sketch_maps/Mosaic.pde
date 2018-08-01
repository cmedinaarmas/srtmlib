class Mosaic{
  
  //int heights[];
  boolean hotColor = true;
  boolean greenColor = false;
  
  float maxHeight;
  float minHeight;
  int mosaicRows;
  int mosaicCols;
  int sz;
  int r;
  int c;
  int normalize;
  int[] mosaicHeights;    //array of original heights. Usually normalized
  int[] mosaicBuffer;     //array to build neutral map
  //byte[] bufferBytes;
     
  Mosaic(sketch_maps.Block data[], int rows, int cols, float max, float min, int blockSize, int norm){
   println("Creating moisaic... "+millis());
   maxHeight = max;
   minHeight = min;
   mosaicRows = rows;
   mosaicCols = cols;
   sz = blockSize;
   r=c= blockSize;
   
   normalize = norm;
   int[] buffer = new int[rows*cols*blockSize*blockSize];
   
    for(int i = 0; i < data.length; i++){      //recover data for each block
      int x = (i % cols);
      int y = (i / cols);
    
      print("X:"+x+" Y:"+y+" ->");
      data[i].printFilename();
    
      int blockData[] = data[i].loadedHeigths;
      data[i].freeLoadedHeighs();

      for(int k=0; k<blockSize*blockSize; k++){
        int val;
        if(normalize==0)  val = (int) blockData[k];
        else              val = (int) ( ( blockData[k] - min ) * 255 / (max - min) );                 //normalize values
        
        int index = kblock2Mosaic( x, y, k, mosaicCols, r, c);
        buffer[index] = val;
      }
    }
  mosaicHeights = buffer;    //store all heights for further processing
  
  buffer = new int[0];
  println("Mosaic data loaded...\t"+millis());
  }
  
  //----------------------------------------------------------------------------
  void storeBwMosaic(int[] buffer, String path){
    PImage img = createImage(mosaicCols*sz, mosaicRows*sz, RGB);
    img.loadPixels();
     
      for(int i=0;i<buffer.length;i++)  
        img.pixels[i] = color(buffer[i], buffer[i], buffer[i]);

    img.updatePixels();
    img.save(path);
    println("Stored BW Mosaic in "+path);
  }
  //----------------------------------------------------------------------------
  void storeColorMosaic(int[] buffer, String path){
    PImage img = createImage(mosaicCols*sz, mosaicRows*sz, RGB);
    img.loadPixels();
    int mosaicRow = mosaicCols*sz;

      
      for(int i=0;i<buffer.length;i++){  
        int hueRange = 360;
        float hue;
        
        if(hotColor) hue = 360 - ( (mosaicHeights[i]- minHeight ) * hueRange / (maxHeight - minHeight) );                  //normalize values
        else if(greenColor) hue = 50 + ( (mosaicHeights[i]- minHeight ) * hueRange / (maxHeight - minHeight) );                  //normalize values
        else hue = ( (mosaicHeights[i]- minHeight ) * hueRange / (maxHeight - minHeight) );                  //normalize values
        float sat = 0.8;
        
        float lumDefaultVal = 0.4;
        float lum = lumDefaultVal;
        float slope_f = 50;    //original value 50
        float maxLumVal = 0.7;
        float minLumVal = 0.05;  //original value 0.05
        
        
        if(i<buffer.length-mosaicRow){          //create shades with luminance
          float delta = ( mosaicHeights[i]-mosaicHeights[i+mosaicRow] );
          
          if((delta==0) && (mosaicHeights[i]>0)){
            lum = lumDefaultVal;
          }
          else if((delta == 0) && (mosaicHeights[i]==0)){
            lum = (int) 0;
          } 
          else{
            lum += delta/slope_f;
            if (lum>maxLumVal)  lum=maxLumVal;
            else if(lum<minLumVal)  lum=minLumVal;
          } 
        }
        else lum = 0.5;
        
        img.pixels[i] = HSL2RGB(hue, sat, lum);
      }
    img.updatePixels();
    img.save(path);
    println("Stored BW Mosaic in "+path);
  }
  //----------------------------------------------------------------------------
  void storeRawHeightsMosaic(String path){
    storeBwMosaic(mosaicHeights, path);
  }
  //----------------------------------------------------------------------------
  void storeMosaicBytes(String path){
    println("Storing mosaic heights \t"+ millis());
    PrintWriter output;
    output = createWriter(path); // Create a new file    
    output.println(mosaicRows);
    output.println(mosaicCols);
    output.println(sz);
    output.println(mosaicHeights.length);    

    for(int i=0;i<mosaicHeights.length;i++){    
      output.println(mosaicHeights[i]);
    }
    output.flush(); // Writes the remaining data to the file
    output.close(); // close the file

    println("Mosaic heights stored \t"+millis()+" @ "+path+" ");

    //println("Storing Mosaic Bytes... "+ millis());
    //saveBytes(path, (byte)mosaicHeights);
  }
  //----------------------------------------------------------------------------
  void storeShadedReliefMosaic(String path){
   
    println("Storing Neutral Mosaic... "+ millis());
    int minPixelval = 0;
    int maxPixelval = 255;
    int basePixelval = 135;
    int val = 0;
    int slope = 1;
    int slope_f = 4;    //used 5
    int lastMosaicRow = mosaicHeights.length-mosaicCols*sz;
    int mosaicRow = mosaicCols*sz;
    int[] buffer = new int[mosaicRows*mosaicCols*sz*sz];
 
    println("EXPERIMENTAL ZERO HEIGHT COLORING TEST");
    //------------------------------------------------
    for(int i=0;i<mosaicHeights.length;i++){
      
        if(i<lastMosaicRow){                                           //avoid last row
          int delta = mosaicHeights[i] - mosaicHeights[i+mosaicRow];   //compare with pixel below

          if( (delta == 0) && (mosaicHeights[i]>0)){
            val = (int) basePixelval;
          }
          else if((delta == 0) && (mosaicHeights[i]==0)){
            val = (int) 50;
          }
          else{
            val = (int)(basePixelval+delta*slope_f);
            if (val>maxPixelval)  val=maxPixelval;
            else if(val<minPixelval)  val=minPixelval;
          } 
          
       }
       buffer[i]= val;
    }
    mosaicHeights = new int[0];
    
    //bufferBytes = byte(buffer);
    mosaicBuffer = buffer;
    buffer = new int[0];
    
    
    println("Exec System.gc()");
    System.gc();
    
    //store data
    //storeMosaicBytes(bufferBytes);
    storeBwMosaic(mosaicBuffer, path);
    
    //release stored memory
    //bufferBytes = new byte[0];
    mosaicBuffer = new int[0];
    println("Store neutral mosaic DONE "+millis());
  }
  //----------------------------------------------------------------------------
    void storeColoredReliefMosaic(String path){
   
    println("Storing Colored Mosaic... "+ millis());
    mosaicBuffer = mosaicHeights;
   // mosaicBuffer = new int[0];
    
    
    println("Exec System.gc()");
    System.gc();
    
    //store data
    //storeMosaicBytes(bufferBytes);
    storeColorMosaic(mosaicBuffer, path);
    
    //release stored memory
    //bufferBytes = new byte[0];
    mosaicBuffer = new int[0];
    println("Store Color mosaic DONE "+millis());
  }
  //----------------------------------------------------------------------------
int kblock2Mosaic(int x, int y, int k, int cols, int r, int c){

  int kM = k%c;
  if (kM<0) kM = kM+c;  
  int kD = int(floor(float(k)/float(c)));
  int kMosaic = c*(x + cols*(y*r + kD)) + kM ;        //compute mosaic k with x displacement
 
  return kMosaic;
}
 //----------------------------------------------------------------------------
 void flat2black(){
  int[] buffer = mosaicHeights;    //store heights in a buffer
  int rows = mosaicRows*sz;
  int cols = mosaicCols*sz;
  
   mosaicHeights = buffer;
 }
 
 
  //----------------------------------------------------------------------------
 // Given H,S,L in range of 0-360, 0-1, 0-1  Returns a Color
color HSL2RGB(float hue, float sat, float lum){
    float v;
    float red, green, blue;
    float m;
    float sv;
    int sextant;
    float fract, vsf, mid1, mid2;
 
    red = lum;   // default to gray
    green = lum;
    blue = lum;
    v = (lum <= 0.5) ? (lum * (1.0 + sat)) : (lum + sat - lum * sat);
    m = lum + lum - v;
    sv = (v - m) / v;
    hue /= 60.0;  //get into range 0..6
    sextant = floor(hue);  // int32 rounds up or down.
    fract = hue - sextant;
    vsf = v * sv * fract;
    mid1 = m + vsf;
    mid2 = v - vsf;
 
    if (v > 0)
    {
        switch (sextant)
        {
            case 0: red = v; green = mid1; blue = m; break;
            case 1: red = mid2; green = v; blue = m; break;
            case 2: red = m; green = v; blue = mid1; break;
            case 3: red = m; green = mid2; blue = v; break;
            case 4: red = mid1; green = m; blue = v; break;
            case 5: red = v; green = m; blue = mid2; break;
        }
    }
    return color(red * 255, green * 255, blue * 255);
}
//----------------------------------------------------------------------------
  
}