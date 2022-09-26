import os
import xml.etree.ElementTree as ET
import time
import glob
import sys

avp=""
  
def fileCheck(SceneName,fname):

    flag=False
    path="./TCases/"+SceneName
    files=glob.glob(path +"/**/*.py",recursive=True)
    
    for name in files:
      if fname.lower() in name.lower():
        flag=True
      else:
        print("Warning...!!! Enter the correct TestScript Name")
    return flag

def show_report():
  print("in show report")          
  file1 = open("/path.txt","r")
  print("Detection Success Rate(%) of Autoware : ")
  print("Detection Range of LGSVL(meters)      : ")
  print("Detection Range of  Autoware(meters)  : ")

def Poly_Runner(validation,SceneName,TestScript):          
     print("Running Scene",SceneName,TestScript)
     pid = os.getpid()
     global avp
  
     if True:
          dict={"Detection":"validate_p.sh",
                "Control":"control_validate_p.sh",
                "Localization":"validate_local.sh",
                "PathPlanning":"validate_pathplannerNode.sh"}
        
          nr="./support_files/NodeRunner.sh " + dict[validation]
          os.system(nr)
          print("nr::",nr)
          reportpath = "./TCReports.sh " + TestScript
          os.system(reportpath)
          #avp
          if avp=="AVP":
            print("Launching Rviz in AVP Demo..")
            os.system('./avp_launch.sh')
            time.sleep(4)       
          path="./TCRunner.sh " + SceneName +" "+ TestScript
          os.system(path)
          time.sleep(4)
          if avp=="AVP":   
              print("Setting Intial Position in Rviz...")     
              os.system('./q_initialPos.sh')
              time.sleep(2)
              print("Setting Goal Position in Rviz...")
              os.system('./q_goalPos.sh')
              
          
          time.sleep(30)  
          input("Press Enter to generate report : ")  
          dt={"Detection":"./q_perception_val_script.sh",
              "Control":"./control_val_script.sh",
              "Localization":"./localization_validate.sh",
              "PathPlanning":"./path_planner_validate.sh"}

          os.system(dt[validation]) 
          os.system('./support_files/stop.sh')
          #show_report()      
     else:
        print("Error TestCase file not found...!!!!!")

def main():

   if len(sys.argv) < 2:
     print("\nEnter the test file Name..Eg:-->python mainScript.py test1.xml\n")
   mytree=ET.parse(sys.argv[1])
   #mytree=ET.parse('test2.xml')
   myroot=mytree.getroot()
   print("*********************************PolyVerif_Shell***********************************\n")
   print("ade hasbeen stated please wait for while...")
   print("Once LGSVL started go to any web browser and start localHost http://localhost:8080/#/Simulations\n")
   time.sleep(5)
   os.system('./WUI_start_ade.sh')
   time.sleep(30)
   Testcase=myroot[0].tag
   path=myroot[0][4].attrib
   SceneName=path["name"]
   Ts=myroot[0][1].attrib
   TestScript=Ts["Location"]
   val=myroot[0][2].attrib
   validation=val["Type"]
   avp=myroot[0][3].text

   Poly_Runner(validation,SceneName,TestScript)
   print(".")
  
  




if __name__ == "__main__":  
  
   #try:
      main()
  # except:
      print("Something went wrong..")
   #finally:
      print("The Process is finished.")