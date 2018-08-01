/*
Version 4 sketch_maps
Updated to OSX: One additional file detected

corrected gap in block boundaries
addded capability to treat automaticaly w or e lat files
Bulk download application and downloads in C:\Program Files\bda\
modified function in Mosaic obj to store heights in txt file
*/
import java.awt.Toolkit; 

void setup(){

//----------------------------------------------------------------
int blockSize;
int normalize = 0;
String mosaicPath = "/Users/cm/Documents/Processing/output/mosaicRaw.png";    //image storage path
String txtPath = "/Users/cm/Documents/Processing/output/heights.txt";         //heights file path
String base;
BlockList mapFiles;

int source = 7;    //define source of data

// 0: Mosaic arc1 1: test arc1  2: Mosaic arc3  3: test arc3   4: Montserrat 
// 5: Geneve 6:Baltoro 7:CentralAmerica 8:Alps
//----------------------------------------------------------------

switch(source){
  
  case 0:   base = "/Users/cm/Documents/Processing/digitalElevation/1arc/"; 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/1arc");
            blockSize = 3600;
            break;
  
  case 1:   base = "/Users/cm/Documents/Processing/digitalElevation/1arcTest/";   //1 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/1arcTest");
            blockSize = 3600;
            break;
  case 2:
            base = "/Users/cm/Documents/Processing/digitalElevation/3arc/";        //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/3arc");
            blockSize = 1200;
            break;
  case 3:    
            base = "/Users/cm/Documents/Processing/digitalElevation/3arcTest/";      //3 arc resolution
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/3arcTest");
            blockSize = 1200;
            break;
  case 4:
            base = "/Users/cm/Documents/Processing/digitalElevation/montserrat/"; //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/montserrat");
            blockSize = 1200;
            break;
  case 5: 
            base = "/Users/cm/Documents/Processing/digitalElevation/geneve/"; //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/geneve");
            blockSize = 1200;
            break;   
  case 6: 
            base = "/Users/cm/Documents/Processing/digitalElevation/baltoro/";   //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/baltoro");
            blockSize = 1200;
            break;
  case 7: 
            base = "/Users/cm/Documents/Processing/digitalElevation/ca/";       //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/ca");
            blockSize = 1200;
            break;        
            
   case 8: 
            base = "/Users/cm/Documents/Processing/digitalElevation/alps/";       //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/alps");
            blockSize = 1200;
            break;
            
  case 9: 
            base = "/Users/cm/Documents/Processing/digitalElevation/guadaloupe/";       //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/guadaloupe");
            blockSize = 1200;
            break;
            
  default:
            base = "/Users/cm/Documents/Processing/digitalElevation/montserrat/"; //3 arc resolution 
            mapFiles = new BlockList("/Documents/Processing/digitalElevation/montserrat");
            blockSize = 1200;
            break;
}


String[] files = mapFiles.getFileList();
int rows = mapFiles.getMosaicRows();
int cols = mapFiles.getMosaicCols();
int blocks = rows*cols;

String[] path = new String[2];
path[0] = base;

println("Processing "+files.length+" Blocks");
Block[] mapBlock = new Block[files.length];
  
  for(int i = 0; i < files.length; i++){
    path[1] = files[i];                          //specify files to load
    mapBlock[i]= new Block(path, blockSize);     //load data from files
    mapBlock[i].byte2height();                   //compute heights
    //mapBlock[i].shadedRelief();
    //mapBlock[i].rawHeights(1);                //uses normalization parameter
    //mapBlock[i].saveBuffer2Image();
  }

 
  //detect global max
  float min = 10000;
  float max = 0;
  
  for(int i = 0; i < files.length; i++){
   if(mapBlock[i].min<min) min = mapBlock[i].min;
   if(mapBlock[i].max>max) max = mapBlock[i].max;
  }
  println("Global Max: "+max+" Global Min: "+min);

  
  Mosaic mapMosaic = new Mosaic(mapBlock, rows, cols, max, min, blockSize, normalize);
  //mapMosaic.storeRawHeightsMosaic(mosaicPath);          //raw heights, must be normalized
  //mapMosaic.storeShadedReliefMosaic(mosaicPath);        //gray colored shaded relief
  mapMosaic.storeColoredReliefMosaic(mosaicPath);      //generate color shaded mosaic
  //mapMosaic.storeMosaicBytes(txtPath);          //gerenarate a txt file with heights

 
 
println("sketch_maps DONE "+millis()+" ms");
Toolkit.getDefaultToolkit().beep();
}

void draw(){
  text("word", 10, 30); 
  exit();
}