class BlockList{
  String[] children;
  String[] list;
  int childCount = 0;
  String cLong;
  String cLat;
  File dir;
  
  int rows;
  int cols;
  int voidBlocks;
  String[] filenameRef;
  
  ///-------------------------------
  BlockList(String path){
    
    dir = new File((System.getProperty("user.home"))+path); 
    children = dir.list();
    println(children);
    int fileNum = children.length -1;
    
    if (children == null) {
      println("ERROR: files not found");
      return;
    } 
    
    else {
      //println(children.length+" files found..."); 
       println(fileNum+" files found..."); 
      
      //declare variables to store lat and long extremes of mosaic
      int max_long = 0;
      int min_long = 90;
      int max_lat  = 0;
      int min_lat  = 180;
      //problem in OSX, fist detected file is not a dataFile. Partial Solution: Skip first file
      for (int i=1; i<children.length; i++){
      
        String[] q =  splitTokens(children[i],"_");   //split latitude and longitude
        
        //String[] temp_long = split(q[0],"n");         //remove N and W
        //String[] temp_lat = split(q[1],"w");
        //String[] temp_lat = split(q[1],"e");      //needed for geneve
        
        
        String[] temp_long;
        temp_long = split(q[0],"n");
        cLong = "n";
        int stringLenLon = temp_long.length;
        
        if( stringLenLon == 1 ){
          temp_long = split(q[0],"s"); 
          cLong = "s";
         }
     
        String[] temp_lat;
        temp_lat = split(q[1],"w");
        cLat = "w";
        int stringLenLat = temp_lat.length;
     
        if( stringLenLat == 1 ){
           temp_lat = split(q[1],"e");  
           cLat = "e";
        }
        println(q[0] +" "+ q[1] + " "+cLong +" "+ cLat + " " + temp_long[1]+ " " + temp_lat[1]);
        
        filenameRef = q;
      
        int longitude = int(temp_long[1]);          //convert to integer values
        int latitude =  int(temp_lat[1]);
      
        if(max_long < longitude) max_long = longitude;
        if(min_long > longitude) min_long = longitude;
      
        if(max_lat < latitude) max_lat = latitude;
        if(min_lat > latitude) min_lat = latitude;
        
  
      }
    
      rows = (max_long-min_long+1);
      cols = (max_lat-min_lat+1);
      int blocks = rows*cols;
      //voidBlocks = blocks - children.length;
      voidBlocks = blocks - fileNum;
      
      String[] fileList = new String[blocks];   //list to hold all filenames 
      String[] filename = new String[9];        //n13_w089_3arc_v2.bil
      filename[0] = cLong;
      filename[2] = "_";
      filename[3] = cLat;
      //filename[2]="_e";    //needed for geneve
    
      //filename[4]="_3arc_v2.bil";
      filename[5]="_";
      filename[6]=filenameRef[2];
      filename[7]="_";
      filename[8]=filenameRef[3];
    
      int k=0;
    
      if(cLat == "w"){
        for(int lo = max_long; lo>=min_long;lo--){
          for(int la = max_lat; la>=min_lat;la--){
            filename[1]=nf(lo, 2);    //add values
            filename[4]=nf(la, 3);
            fileList[k]=join(filename,"");
            k++;
      }}}
    
      else{
        for(int lo = max_long; lo>=min_long;lo--){
          for(int la = min_lat; la<=max_lat;la++){
            filename[1]=nf(lo, 0);    //add values
            filename[4]=nf(la, 3); 
            fileList[k]=join(filename,"");
            k++;
      }}}
      
      list = fileList;
      
      println("Longitude N "+min_long+":"+max_long);
      println("Latitude  W "+min_lat+":"+max_lat);
      println("Rows:"+rows+" Cols:"+cols);
      println("Blocks "+blocks);
      println("Void Blocks "+voidBlocks);
      printArray(fileList); 
   
  }
    
  }
  ///--------------------

  String[] getFileList(){
    return list;
  }  
  
  int getMosaicRows(){
    return rows;
  }
  
  int getMosaicCols(){
    return cols;
  }
  
  void printList(){
    printArray(list);
  }
  
}