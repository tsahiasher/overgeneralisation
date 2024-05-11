<?php 
session_start();
$ses_id=session_id();
ini_set('display_errors', 'Off');

//id for each user doing experiment

//echo "ID".$ses_id;

?>
<html>
<head>
<title>exp</title>

<script src="https://code.jquery.com/jquery-1.9.1.min.js"></script>
<!-- Bootstrap -->
<link href="bootstrap.css" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">

<script>
function DoLoad(){};

</script>



<style>
.button {
padding:12px;
    background-color: #dcdcdc;
border: 1px solid #666;
color:#000;
    text-decoration:none;
}

.btn-sm {
    font-size: 7px;
    border-radius: 3px;
width:14%;  
    
}		

.like{
width: 50px;
height: 50px;
    background-color: FFFF33;
position:absolute;
left:1000px;
top:150px;
    font-family:"Times New Roman";

}


.previousTrialWin{

}

.nextStage{
width: 200px;
height: 50px;
    background-color: FFFF33;
position:absolute;
left:1050px;
top:150px;
    font-family:"Times New Roman";

}

.feedbackOdd{
width: 250px;
height: 35px;
color: black;
    background-color: FFFF33;
border: 2px; 
    border-style: solid;
    border-color:grey;
position:absolute;
left:1100px;
top:240px;
    font-family:"Times New Roman";
    text-decoration: blink;
    
}
.blink {
    text-decoration: blink;
}
</style>

</head>
<body  onload="DoLoad();">

<div height="100%" style="background:black;">
<img src="smiley.jpeg" width="80px" style="display:none">

<img src="sadsmiliey2.jpeg" width="80px" height="80" style="display:none">

<TABLE BORDER="0" width="100%"  height="100%">
<TR align="center">


<?php 

#error_reporting(E_ALL);
#ini_set('display_errors', 1);

#$_POST = array();
if($trialPart2 <= 31){
    //current time
    $timer = microtime(true);
    $string='?';
    $font=dirname(__FILE__) .'/arial.ttf';
    //the parameters
    //parameter get the in
    //mation which button clicked right or left

    $numDomCircles=0;
    $NumCirclesOdd=0;
    // create a 500*500 image
    $img = imagecreatetruecolor(400, 400);
    // allocate some colors
    //imagesetthickness($img, 10);
    $blue = imagecolorallocate($img,   65, 105,   225);
    $red  = imagecolorallocate($img,   220,   0, 0);
    $green = imagecolorallocate($img,   50, 205,   50);
    $white = imagecolorallocate($img,  255,255,255 );
    $yellow  = imagecolorallocate($img,   252,227,7);
    $black = imagecolorallocate($img, 0, 0, 0);

    $blueSt = '#4169e1';
    $redSt  = '#dc0000';
    $greenSt='#32cd32';
    $whiteSt = '#FFFFFF';
    $yellowSt  = '#FCE307';

    //build arrays with colors
    $stringColorsArray = array("blue","red","green","white","yellow");
    $Array = array($blueSt,$redSt,$greenSt,$whiteSt,$yellowSt);
    $paramColorsArray = array($blue,$red,$green,$white,$yellow);
    
    $list=array();
    $listPart2=array();
    $array1or6=array();
    $array1or6=array();
    $coordArray= array();
    $arrayPart2=array();
    $arrayIfSucsses=array();
    $paramArrayWithoutThisColors=array();
    $colorsArrayWithoutThisColors=array();
    $stringColorsArrayWithoutThisColors=array();
    $endExp=array();
    //if press button (trial>1)
    if(!$_POST){
        
        //insert to Data Base  data of the STAI test
        $trialPart2=0;
        
        $count=0;
        $count1=0;
        $counter9=0;
        $counter9_1=0;
        $counter9_2=0;
        $counter9_3=0;
        $counter9_4=0;
        $counter9_0=0;
        $counter9_5=0;
        $counter=1;
        $trial=1;
        $origtrial=1;
        $howManyParamColor2=0;
        $howManyParamColorDom=0;
        $trialToTable=1;	
        $howSucc=0;
        $countPositive=0;
        $sucsses="no";
        $leftOrRightButton=0;
        $counterLenArray=0;
        $trialPart2=1;
        $flag="no";
        $feedback=1;
        $origFeedback=0;
        $trialEvenFeedbacks=0;
        $replaceImage = 0;
        $ans=1;
        $ansTr=1;
        $numberDom=0;
        $signal="no";
        $counter2=1;
        $counterMinority=0;
        $counterMajority=0;
        $counterMajorityPart2=0;
        $counterMinorityPart2=0;
        $imagecounter=0;
        $numRound = 1;

        $array1or6=threeCircles($count,$count1);

    }else{?>
        
        <?php //echo "<br>";
        //$link = mysql_connect('localhost', 'tsirkinlea', '25364964');

        //$db_selected = mysql_select_db('circlesdb', $link);
        // mysql_select_db('circlesRingdb', $link);
        if($trial==2){	
            $newprevstringColorDom==$prevstringColorDom=$_POST["hiddenStrColorDom"];
            $newstringColor==$stringColor=$_POST["hiddenStrColor"];
        }
        $leftOrRightButton = $_POST["whichButtonPressed"];
        $prevleftOrRightButton = $_POST["whichButtonPressed"];
        $newprevleftOrRightButton = $_POST["hiddenPrevleftOrRightButton"];
        $trial=$_POST["hidden"];
        //echo "TRIAL".$trial;
        $origtrial=$trial;
        $origFeedback=$_POST["hiddenFeedback"];
        $feedback=$_POST["hiddenFeedback"];
        $trialToTable=$_POST["hiddentrialToTable"];
        if($feedback==0 && $trial>1){
            $feedback=1;
        }else{
            $feedback=0;
        }

        if($feedback==0){
            $trial=$trial+1;

        }
        if($feedback==1){
            $trialToTable=$trialToTable+1;
            
        }
        $howSucc=$_POST["hiddenHowSuccess"];
        $numRound=$_POST["numRound"];
        $imagecounter=$_POST["imagecounter"];
        $trialPart2=$_POST["hiddenTrialPart2"];
        $countPositive=$_POST["hiddenCountPositive"];
        $stringColorDom=$_POST["hiddenStrColorDom"];
        $prevstringColorDom=$_POST["hiddenStrColorDom"];
        $newprevstringColorDom=$_POST["hiddenPrevstringColorDom"];
        $stringColor=$_POST["hiddenStrColor"];
        $prevstringColor=$_POST["hiddenStrColor"];
        $newstringColor=$_POST["hiddennewstringColor"];
        $counterLenArray=$_POST["hiddenCounterLenArray"];
        $flag=$_POST["hiddenFlag"];
        $trialEvenFeedbacks=$_POST["hiddenTrialEvenFeedbacks"];
        $colorPrev=$_POST["hiddenColorCircle"];
        $prevSmiley=$_POST["hiddenprevSmiley"];
        $sucsses=$_POST["hiddensucsses"];
        $counter=$_POST["hiddenCounter"];
        $number=$_POST['hiddenYourAnswer'];
        $correct=$_POST['hiddenCorrectAnsw'];
        $counter2=$_POST['hiddenCounter2'];
        $numberDom=$_POST['hiddennumberDom'];
        $prevnumberDom=$_POST["hiddennumberDom"];
        $newprevnumberDom=$_POST["hiddenprevnumberDom"];
        $number1=$_POST["hiddennumber1"];
        $prevsNumber1=$_POST["hiddennumber1"];
        $newprevsNumber1=$_POST["hiddenprevnumber1"];
        $origflagst7=$_POST['hiddenFlagst7'];
        $prevorigflagst7=$_POST['hiddenFlagst7'];
        $neworigflagst7=$_POST['hiddenprevFlagst7'];
        $time1=$_POST['hiddenTime'];
        $counterMajority=$_POST['hiddenCounterMajority'];
        $counterMinority=$_POST['hiddenCounterMinority'];
        $counterMajorityPart2=$_POST['hiddenCounterMajorityPart2'];
        $counterMinorityPart2=$_POST['hiddenCounterMinorityPart2'];
        $count=$_POST['hiddenCount'];
        $count1=$_POST['hiddenCount'];
        $counter9=$_POST['hiddenCounter9'];
        $counter9_1=$_POST['hiddenCounter9_1'];
        $counter9_2=$_POST['hiddenCounter9_2'];
        $counter9_3=$_POST['hiddenCounter9_3'];
        $counter9_4=$_POST['hiddenCounter9_4'];
        $counter9_5=$_POST['hiddenCounter9_5'];
        $counter9_0=$_POST['hiddenCounter9_0'];
        $prevtime=$_POST['hiddenTime'];
        $newprevTime=$_POST['hiddenprevTime'];
        $howManyParamColor2=$_POST['hiddenhowManyParamColor2'];
        $howManyParamColorDom=$_POST['hiddenhowManyParamColorDom'];

        if($feedback == 0){
            if($trialEvenFeedbacks >10){
                $trialEvenFeedbacks=$trialEvenFeedbacks	+1;
            }
            //echo "leftOr RBut".$leftOrRightButton;
            if($origFeedback==1){
                $arrayIfSucsses=giveFeedback($stringColorDom,$stringColor,$countPositive,$sucsses,$leftOrRightButton,$trial,$trialEvenFeedbacks,$howSucc,$trialPart2,$numberDom,  			$number1,$flagst7);
                $countPositive=$arrayIfSucsses[0];
                $sucsses=$arrayIfSucsses[1];	
            }

            ?>
            
            <script>
            
            var timer=setTimeout(clickAutoButton,1000);
            
            function clickAutoButton(){
                var myForm=document.getElementById("myForm");
                myForm.submit(); 
                myStopFunction();
            }
            function myStopFunction(){
                clearTimeout(timer);
            }
            
            </script>  
            <?php 


        }
    }
    file_put_contents("tmp.txt",$howSucc." ".$numRound." ".$imagecounter."\n", FILE_APPEND);
    
    if (($howSucc==0 && $imagecounter==400) || ($howSucc==1 && $imagecounter==1000) || ($howSucc==2 && $imagecounter==2000) || 
    ($howSucc==3 && $imagecounter==3000) || ($howSucc==4 && $imagecounter==6000) || ($howSucc==5 && $imagecounter==3000)){
        if ($howSucc==5){
            $howSucc = 6;
        }
        $howSucc++;
        $_POST["howSucc"] = $howSucc;
        $imagecounter = 0;
        $_POST["imagecounter"] = $imagecounter;
    }
    if ($howSucc==7 && $imagecounter==2000){
        if ($numRound==6) exit(400);
        $numRound++;
        $_POST["numRound"] = $numRound;
        $imagecounter = 0;
        $_POST["imagecounter"] = $imagecounter;
    }
    
    if($feedback==1 && $_POST){
        $time = round(($timer-$newprevTime-1.8),3);

        if($howSucc <= 6){
            if($howSucc>=0 && $countPositive<8 && $howSucc<=6 ){

                if($howSucc==0){
                    //picture with 3 circles. One in one color, 2-other color Only 2 colors and only 4 positions.
                    $array1or6=threeCircles($count,$count1);
                }
                
                if($howSucc==1){
                    //picture with 3 circles. One in one color, 2-other color. Only 2 colors. all positions.
                    $array1or6=threeCircles($count,$count1);
                }

                if($howSucc==2){
                    //picture with 7 circles. One in one color, 6-other color. All colors. all positions.
                    $array1or6=threeOtherCircles();
                }

                if($howSucc==3){
                    //picture with 7 circles. All variante (1,6;2,5;3,4;). All colors. all positions.
                    $array1or6=stage4IncreaseMax();
                }
                if($howSucc==4){
                    //picture with 7,9 or 11 circles (randomally). All variante (1,6;2,5;3,4;). All colors. all positions.
                    $array1or6=stage5IncreaseMaxAndMin();
                }
                //stage 7 include 2 kinds of images: three colors and 2 colors and display it randomally
                if($howSucc==5 || $howSucc==6){
                    //picture with 7,9 or 11 circles (randomally). All variante (1,6;2,5;3,4;). All colors. all positions.
                    $arrayPart2=stage6and7_3colors();
                }
                
                
            }else{?>
                <div class="like">
                <img src="ylike.jpeg"  width="40px" height="55px">
                </div>
                <div class="nextStage">
                <font size="4">Congratulations, You have reached the Next Stage!</font>
                </div>
                <?php if($howSucc>=0 && $countPositive==8 && $howSucc<=6){
                    $countPositive=0;
                    $howSucc++;
                    
                    if($howSucc==1){
                        $array1or6=threeCircles($count,$count1);

                    }if($howSucc==2){
                        $array1or6=threeOtherCircles();
                    }

                    if($howSucc==3){
                        $array1or6=stage4IncreaseMax();

                    }
                    if($howSucc==4){
                        $array1or6=stage5IncreaseMaxAndMin();
                    }
                    
                    if($howSucc==5 || $howSucc==6){
                        $arrayPart2=stage6and7_3colors();
                    }		
                    
                    
                    
                    //if $countPositive==8...
                }
                //else
            }
            //if $howSucc <= 8
        }

        //after finish the part 1 the experiment, we will add 10 trials more then get the  even trial
        //part 2 of the experiment. 3 color circles
        
        if($howSucc>=7 && $trialPart2<=31){
            //$trialPart2=$trialPart2+1;
            //$arrayPart2=6and7_3colors();
            $arrayPart2=stage8_3colors($counter9,$counter9_0,$counter9_1,$counter9_2,$counter9_3,$counter9_4,$counter9_5,$numRound);
            $colorCenterLastPart=$arrayPart2[4];
            $counter9=$arrayPart2[5];
            $counter9_0=$arrayPart2[6];
            $counter9_1=$arrayPart2[7];
            $counter9_2=$arrayPart2[8];
            $counter9_3=$arrayPart2[9];
            $counter9_4=$arrayPart2[10];
            $counter9_5=$arrayPart2[11];
            if($trial%2 == 0){
                $flag="yes";
            }else{
                $flag="no";
            }
        }if($trialPart2==31){
            if($trialPart2==31 && $origFeedback==1){
                sleep(0);
            }
            // ncurses_erase();?>
            <?php }
    }?>


    <td colspan="5" height="10px" >
    
    <?php session_start();?>
    <?php if($trialPart2<2){?>
        <div class="stagePlace">
        <?php if($howSucc==0){?>
            
            <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;1/8</h2></font></center>
            <?php }
        
        if($howSucc==1){?>
            <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;2/8</h2></font></center>
            <?php }
        if($howSucc==2){?>
            <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;3/8</h2></font></center>
            <?php }
        if($howSucc==3){?>
            <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;4/8</h2></font></center>
            <?php }
        if($howSucc==4){?>
            <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;5/8</h2></font></center>
            <?php }
        if($howSucc==5){?>
            <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;6/8</h2></font></center>
            <?php }
        if($howSucc==6){?>
            <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;7/8</h2></font></center>
            <?php }
        
        
    }
    if($trialPart2>=2 && $trialPart2<32){?>
        <center><h2 style="font-family:verdana;"><font color="yellow">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;8/8</h2></font></center>
        <?php }
    if($trialPart2==32){?>
        <center><h2 style="font-family:verdana;"><font color="black">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;STAGE&nbsp;&nbsp;&nbsp;&nbsp;8/8</h2></font></center>
        <?php }
    ?>
    </div>
    </td>
    </tr>

    <?php if($howSucc>=6){?>
        <div class="feedbackOdd">
        <font size="4">&nbsp;&nbsp;&nbsp;Feedback in odd trials only</font>
        </div>
        <?php }?>


    <tr  valign="top">


    <td width="13%"   valign="top">

    </td>

    <TD width="18%"  >

    </td>
    <?php if(!$_POST || $feedback==1){?>
        <TD width="29%"  height="333px"   align="center" valign="center">
        <br><br>
        <?php }else{?>
        <TD  width="29%" height="333px"  align="center" valign="center">
        <br><br>

        <?php }
    //height="250px"
    //height="100px"
    //height="100px"
    //height="80px"

    if((!$_POST) || ($feedback==1 || $flag="no" || $flag="yes")){
        $counterColorDom=0;
        $coiunterColor2=0;
        if($howSucc<2){
            $numRoundColor=round(mt_rand(1.1,2.98),PHP_ROUND_HALF_DOWN);
            //if()
            if($numRoundColor==1){
                $count3++;
                $numColorDom=1;
                $numColor2=3;
            }else{
                $numColorDom=3;
                $numColor2=1;
            }
        }else{
            $numColorDom=round(mt_rand(0,4));
            $numColor2=round(mt_rand(0,4));
            //choose the second color in the paramColorsArray
            if($numColor2==$numColorDom){
                if($numColorDom!=4){
                    $numColor2=$numColor2+1;
                }else{
                    $numColor2=0;
                }

            }
            if($numColorDom==1 && $numColor2==2){
                $numColor2=3;
            }
            if($numColorDom==2 && $numColor2==1){
                $numColorDom=3;
            }
            if($numColorDom==4){
                $numColor2=0;
            }
            if($numColor2==4){
                $numColorDom=0;
            }
            // end else if($howSucc<3)
        }
        $paramColorDom=$paramColorsArray[$numColorDom];
        $stringColorDom=$stringColorsArray[$numColorDom];
        $colorDom=$colorsArray[$numColorDom];
        $paramColor2=$paramColorsArray[$numColor2];
        $stringColor2=$stringColorsArray[$numColor2];
        $color2=$colorsArray[$numColor2];
        //echo"<br>";
        //echo "stringcolordom".$stringColorDom;
        //echo"<br>";
        //echo "stringcolor2".$stringColor2;
        //stages, 1-6 and 7,8 if $flagst7==0
        if($howSucc<=4) {
            if($howSucc ==0){
                $num1= $array1or6[0];
                $numColor2Circles=$array1or6[2];
                $numDomCircles=$array1or6[1];
                

            }
            if($sucsses=="no" && $howSucc<=1 && $POST){
                $stringColorDom=$prevstringColorDom;
                $stringColor=$prevstringColor;
            }


            if($howSucc ==1){?>
                <?php $num1=$array1or6[0];
                $numColor2Circles=$array1or6[2];
                $numDomCircles=$array1or6[1];
            }

            if($howSucc==2){
                $num1=$array1or6[0];
                $numColor2Circles=$array1or6[2];
                $numDomCircles=$array1or6[1];
            }

            if($howSucc==3){
                $num1=$array1or6[0];
                $numColor2Circles=$array1or6[2];
                $numDomCircles=$array1or6[1];

            }

            //stage 6 or stages, 7 // 8 if  $flagst7==0
            if($howSucc==4){
                $num1=$array1or6[0];
                //now, let's draw dom circles that will be most
                $numColor2Circles=$array1or6[2];
                $numDomCircles=$array1or6[1];
            }

            if($howSucc<3){
                //number circles
                $a=144;
                $m=5;
                //celsius
                $ans=360/$m;
                $c=$ans;
                //angle
                $random=mt_rand(0,4);
                if($howSucc==1 || $howSucc==2){
                    $a=$c*$random;
                }
                //radius
                $r=130;
                $centerX=350;
                $centery=350;

            }
            if($howSucc==3 || $howSucc==4){
                //number circles
                $m=$array1or6[0];
                
                //number most of union color 
                $md=$numDomCircles;
                //	echo "domCirc".$md;
                //number the others
                $od=$numColor2Circles;
                //  echo "num2Circ".$od;
                //celsius
                $ans=360/$m;
                $c=$ans;
                //angle
                $random=mt_rand(0,$m-1);
                $a=$c*$random;
                //radius
                $r=130;
                //echo"random".$random;
            }

            if($origFeedback==0){
                $colorNumber=round(mt_rand(1.1,2.98),PHP_ROUND_HALF_DOWN);
                
                if($colorNumber==1){
                    $color=$paramColorDom;
                    $stringColor=$stringColorDom;
                    $howManyParamColorDom++;
                    
                }else{
                    $color=$paramColor2;
                    $stringColor=$stringColor2;
                    $howManyParamColor2++;
                }
                
                if($howManyParamColorDom>4 && $howManyParamColor2<2){
                    $color=$paramColor2;
                }
                if($howManyParamColor2>4 && $howManyParamColorDom<2){
                    $color=$paramColor2;
                }
            }
            
            
            if($howSucc==0){
                imagefilledellipse($img,200 ,182, 360, 360,$color );
                imagefilledellipse($img,200 ,182, 340,340,$black );
                if($sucsses=="no" && $_POST){
                    $stringColorDom=$prevstringColorDom;
                    $stringColor=$prevstringColor;
                }

            }
            if($howSucc==1){
                imagefilledellipse($img,200 ,182, 360, 360,$color );
                imagefilledellipse($img,200 ,182, 340,340,$black );
            }
            
            if($howSucc>=2 && $howSucc<=7){
                // imagefilledellipse($img,300 ,150, 75, 75, $color);
                // imageellipse($img, 300, 150, 290, 290, $color);
                imagefilledellipse($img,200 ,182, 360, 360,$color);
                imagefilledellipse($img,200 ,182, 340,340,$black );
                // imagesetthickness($img, 5);
                
            }
                
            if (!$_POST || $sucsses=="yes" || $sucsses=="no" && $howSucc>=8  ||  $sucsses=="no"){
                if($howSucc<4){ 
                    
                    
                    for ($j=$a; $j<($a+$c*2); $j=$j+$c){
                        if($j>=360){
                            $xCoord=200+$r*sin(($j%360)*3.1415/180);
                            $yCoord=182-$r*cos(($j%360)*3.1415/180);
                        }
                        $xCoord=200+$r*sin($j*3.1415/180);
                        $yCoord=182-$r*cos($j*3.1415/180);
                        
                        imagefilledellipse($img,$xCoord ,$yCoord, 60, 60,$paramColor2);
                        
                        
                    }
                    for($v=$a+$c*2; $v<($a+$c*$m)-1; $v=$v+$c){
                        if ($v>=360){
                            $xCoord=200+$r*sin(($v%360)*3.1415/180);
                            $yCoord=182-$r*cos(($v%360)*3.1415/180);
                        }
                        $xCoord=200+$r*sin($v*3.1415/180);
                        $yCoord=182-$r*cos($v*3.1415/180);
                        imagefilledellipse($img,$xCoord ,$yCoord, 60, 60,$paramColorDom);
                        
                    }
                }
                
                //draw the other circles
                if($howSucc==4  ){
                    
                    for ($k=$a; ($k<$a+$c*($od)); $k=$k+$c){
                        if($k>=360){
                            $xCoord=200+$r*sin(($k%360)*3.1415/180);
                            $yCoord=182-$r*cos(($k%360)*3.1415/180);
                        }
                        $xCoord=200+$r*sin($k*3.1415/180);
                        $yCoord=182-$r*cos($k*3.1415/180);
                        
                        imagefilledellipse($img,$xCoord ,$yCoord, 60, 60,$paramColor2);
                        
                        
                    }
                    for($j=$a+$c*($od); $j<($a+$c*($m))-1; $j=$j+$c){
                        if ($j>=360){
                            $xCoord=200+$r*sin(($j%360)*3.1415/180);
                            $yCoord=182-$r*cos(($j%360)*3.1415/180);
                        }
                        $xCoord=200+$r*sin($j*3.1415/180);
                        $yCoord=182-$r*cos($j*3.1415/180);
                        imagefilledellipse($img,$xCoord ,$yCoord, 60, 60,$paramColorDom);
                        
                    }

                    //end if $howSucc>=4
                }
                
                
                //HERE!!!!!			
                
                // imagettftext($img, 28, 0, 290, 165, $black,$font, $string);

                //save current picture on the session and the old one picture
                
                $oldFile="circles.png";
                $newfilename = 'newcircles1.png';
                $ansTr=$origtrial-1;
                $ansPrevTr=$ansTr-5; 
                if(!$_POST){ 
                    imagepng($img,$newfilename);
                    $_SESSION['img_file_name'] = $newfilename;
                    $_SESSION['old_file'.$origtrial] = $newfilename; 
                    $oldFile=$_SESSION['old_file'.$origtrial];
                    
                } 
                if(isset($_SESSION['img_file_name'])){ 
                    $newfilename = $_SESSION['img_file_name'];
                    
                }
                if(isset($_SESSION['old_file'.$ansTr])){    
                    $oldFile=$_SESSION['old_file'.$ansTr];
                }
                $replaceImage = 0; 
                
                // The first stage of the experiment 
                if($howSucc < 1){ 
                    if($origFeedback == 0 && $sucsses == "yes"){ 
                        $replaceImage = 1; 
                    }
                    if($origFeedback == 0 && $sucsses == "no"){
                        $oldFile=$newfilename;
                        $_SESSION['old_file'.$ansTr] = $oldFile; 
                    }
                    if($origFeedback == 1 && $sucsses == "yes"){ 
                        if(isset($_SESSION['old_file'.$ansTr])){ 
                            $oldFile=$_SESSION['old_file'.$ansTr];
                        }
                    }if($origFeedback == 1 && $sucsses == "no"){ 
                        if(isset($_SESSION['old_file'.$ansTr])){ 
                            $oldFile=$_SESSION['old_file'.$ansTr];
                        }
                    }
                    
                }else{ 
                    // The second and more stage of the experiment 
                    if($origFeedback == 0){ 
                        $replaceImage = 1; 
                    }
                } 
                
                if($replaceImage == 1){ 
                    // remove the old file
                    if(isset($_SESSION['old_file'.$ansPrevTr])){ 
                        unlink($_SESSION['old_file'.$ansPrevTr]); 
                    }
                    $oldFile=$newfilename;
                    $_SESSION['old_file'.$ansTr] = $oldFile; 
                    $newfilename=uniqid().'.png';
                    if($stringColorDom==$stringColor || $howSucc==7 ){
                        $savefilename = "Stage".($howSucc+1)."/1/".$newfilename;
                    }
                    else {
                        $savefilename = "Stage".($howSucc+1)."/0/".$newfilename;
                    }
                    $imagecounter++;
                    $_POST["imagecounter"] = $imagecounter;
                    imagepng($img, $savefilename);
                    imagepng($img, $newfilename);
                    $_SESSION['img_file_name'] = $newfilename;
                } 
                // Free up me 
                imagedestroy($img);
            }
            if(!$_POST || $origFeedback == 1 && $trial<=2){
                echo "<img src='newcircles1.png'>";
            }else{
                echo "<img src=$newfilename>";
            }


        }
    }

    // after 10 times success in sequence in the first stage - pass to the second one.
    // after 10 times in the second stage go to the third stage.
    if($howSucc==5 || $howSucc==6 || $howSucc==7){
        
        //choose number of 3 kinds of curcles
        $num1=$arrayPart2[0];
        $numberDom=$arrayPart2[1];
        $number1=$arrayPart2[2];
        $number2=$arrayPart2[3];

        ////lets create new array without the choose colors the we ca take the 3ird color for the part
        $k=0;
        for($l=0; $l<=4;){
            if(($l!=$numColorDom) && ($l!=$numColor2)){
                $paramArrayWithoutThisColors[$k]=$paramColorsArray[$l];
                $colorsArrayWithoutThisColors[$k]=$colorsArray[$l];
                $stringColorsArrayWithoutThisColors[$k]=$stringColorsArray[$l];
                $k++;
                $l++;

            }else{
                $l++;
            }
        }

        if (($numColorDom==2 || $numColor2==2) && ($numColorDom==3 || $numColor2==3)){
            $paramArrayWithoutThisColors[0]=$paramColorsArray[0];
            $colorsArrayWithoutThisColors[0]=$colorsArray[0];
            $stringColorsArrayWithoutThisColors[0]=$stringColorsArray[0];
            $paramArrayWithoutThisColors[1]=$paramColorsArray[0];
            $colorsArrayWithoutThisColors[1]=$colorsArray[0];
            $stringColorsArrayWithoutThisColors[1]=$stringColorsArray[0];
            $paramArrayWithoutThisColors[2]=$paramColorsArray[0];
            $colorsArrayWithoutThisColors[2]=$colorsArray[0];
            $stringColorsArrayWithoutThisColors[2]=$stringColorsArray[0];
        }
        if (($numColorDom==2 || $numColor2==2) && ($numColorDom!=3 && $numColor2!=3)){
            $paramArrayWithoutThisColors[0]=$paramColorsArray[3];
            $colorsArrayWithoutThisColors[0]=$colorsArray[3];
            $stringColorsArrayWithoutThisColors[0]=$stringColorsArray[3];
            $paramArrayWithoutThisColors[1]=$paramColorsArray[3];
            $colorsArrayWithoutThisColors[1]=$colorsArray[3];
            $stringColorsArrayWithoutThisColors[1]=$stringColorsArray[3];
            $paramArrayWithoutThisColors[2]=$paramColorsArray[3];
            $colorsArrayWithoutThisColors[2]=$colorsArray[3];
            $stringColorsArrayWithoutThisColors[2]=$stringColorsArray[3];
        }
        if (($numColorDom==2 || $numColor2==2) && ($numColorDom==4 || $numColor2==4)){
            $paramArrayWithoutThisColors[0]=$paramColorsArray[0];
            $colorsArrayWithoutThisColors[0]=$colorsArray[0];
            $stringColorsArrayWithoutThisColors[0]=$stringColorsArray[0];
            $paramArrayWithoutThisColors[1]=$paramColorsArray[0];
            $colorsArrayWithoutThisColors[1]=$colorsArray[0];
            $stringColorsArrayWithoutThisColors[1]=$stringColorsArray[0];
            $paramArrayWithoutThisColors[2]=$paramColorsArray[0];
            $colorsArrayWithoutThisColors[2]=$colorsArray[0];
            $stringColorsArrayWithoutThisColors[2]=$stringColorsArray[0];
        }
        if (($numColorDom==4 || $numColor2==4) && ($numColorDom!=3 && $numColor2!=3)){
            $paramArrayWithoutThisColors[0]=$paramColorsArray[3];
            $colorsArrayWithoutThisColors[0]=$colorsArray[3];
            $stringColorsArrayWithoutThisColors[0]=$stringColorsArray[3];
            $paramArrayWithoutThisColors[1]=$paramColorsArray[3];
            $colorsArrayWithoutThisColors[1]=$colorsArray[3];
            $stringColorsArrayWithoutThisColors[1]=$stringColorsArray[3];
            $paramArrayWithoutThisColors[2]=$paramColorsArray[3];
            $colorsArrayWithoutThisColors[2]=$colorsArray[3];
            $stringColorsArrayWithoutThisColors[2]=$stringColorsArray[3];
        }
        $numColor3=round(mt_rand(0.8,2.8),PHP_ROUND_HALF_DOWN);
        $ParamColor3=$paramArrayWithoutThisColors[$numColor3];
        $color3=$colorsArrayWithoutThisColors[$numColor3];
        $stringColor3= $stringColorsArrayWithoutThisColors[$numColor3];
        if($howSucc==5  || $howSucc<=6 && $origFeedback==0 ){
            if($number2==2 && (($number1==3 && ($numberDom==4 || $numberDom==5)) || ($number1==4 && ($numberDom==5 || $numberDom==6)) || ($number1==5 && $numberDom==6 )) || ($number2==3 && ($number1==4 && ($numberDom==5 || $numberDom==6)))){
                $color=$ParamColor3;
                $stringColor=$stringColor3;
            }else{
                $n=round(mt_rand(1.1,2.98),PHP_ROUND_HALF_DOWN);
                if($n==1){
                    $color=$paramColorDom;
                    $stringColor=$stringColorDom;
                }
                if($n==2){
                    $color=$ParamColor3;
                    $stringColor=$stringColor3;
                }
            }
            imagefilledellipse($img,200 ,182, 360, 360,$color);
            imagefilledellipse($img,200 ,182, 340,340,$black );
        }
        if($howSucc>=7){
            if($origFeedback==0){
                if($colorCenterLastPart==1){
                    $color=$paramColorDom;
                    $stringColor=$stringColorDom;
                }
                if($colorCenterLastPart==2){
                    $color=$paramColor2;
                    $stringColor=$stringColor2;
                }
                if($colorCenterLastPart==3){
                    $color=$ParamColor3;
                    $stringColor= $stringColor3;
                }
                imagefilledellipse($img,200 ,182, 360, 360,$color);
                imagefilledellipse($img,200 ,182, 340,340,$black );
                //($img,300 ,150, 75, 75,$color);
                //imagettftext($img, 28, 0, 290, 165, $black,$font, $string);
            }
        }
        if($howSucc==5 || $howSucc==6 || $howSucc==7 ){
            //number circles
            $m=$arrayPart2[0];
            $random=mt_rand(0,$m-1);
            $md2=$arrayPart2[1];
            $od2=$arrayPart2[2];
            $three2=$arrayPart2[3];
        }
        
        //celsius
        $ans=360/$m;
        $c=$ans;
        //angle
        $a=$c*$random;
        //radius
        $r=130;
        //which the place on the ring stopped draw the dom circles.
        $o=$a+$c*$md2;
        //drawing the circles
        for($s=$a; $s<$o; $s=$s+$c){
            if($s>=360){
                $xCoord=200+$r*sin(($s-360)*3.1415/180);
                $yCoord=182-$r*cos(($s-360)*3.1415/180);
            }
            $xCoord=200+$r*sin($s*3.1415/180);
            $yCoord=182-$r*cos($s*3.1415/180);
            imagefilledellipse($img,$xCoord ,$yCoord, 60, 60,$paramColorDom);
        }
        $w=$c*$od2+$o;
        for($y=$o; $y<($c*$od2+$o)-1; $y=$y+$c){
            if($y>=360){
                $xCoord=200+$r*sin(($y-360)*3.1415/180);
                $yCoord=182-$r*cos(($y-360)*3.1415/180);
            }
            $xCoord=200+$r*sin($y*3.1415/180);
            $yCoord=182-$r*cos($y*3.1415/180);
            imagefilledellipse($img,$xCoord ,$yCoord, 60, 60,$paramColor2);
        }
        for($t=$w; $t<$w+$c*$three2-1; $t=$t+$c){
            if ($t>=360){
                $xCoord=200+$r*sin(($t-360)*3.1415/180);
                $yCoord=182-$r*cos(($t-360)*3.1415/180);
            }
            $xCoord=200+$r*sin($t*3.1415/180);
            $yCoord=182-$r*cos($t*3.1415/180);
            imagefilledellipse($img,$xCoord ,$yCoord, 60, 60,$ParamColor3);
        }

        //on this stages the center circle color determined by $n. It will be colored the minimum circles colored or same the maximum color
        //determine what will be the center circle color on the last stage (Parameters received from the function sevenNineElevenPart2)
        //Save the image as 'simpletext.jpg'
        $dom=$stringColorDom;
        $ansTr=$origtrial-1;
        $ansPrevTr=$ansTr-5;
        if(isset($_SESSION['img_file_name'])){
            $newfilename = $_SESSION['img_file_name'];
        }
        if(isset($_SESSION['old_file'.$ansTr])){    
            $oldFile=$_SESSION['old_file'.$ansTr];
        }

        if($origFeedback == 0){
            if(isset($_SESSION['old_file'.$ansPrevTr])){ 
                unlink($_SESSION['old_file'.$ansPrevTr]); 
            } 
            $oldFile=$newfilename;
            $_SESSION['old_file'.$ansTr] = $oldFile; 
            $newfilename=uniqid().'.png';
            if ($howSucc==7)
                $savefilename = "Stage".($howSucc+1).".".$numRound."/1/".$newfilename;
            else if($stringColorDom==$stringColor){
                $savefilename = "Stage".($howSucc+1)."/1/".$newfilename;
            }
            else {
                $savefilename = "Stage".($howSucc+1)."/0/".$newfilename;
            }
            $imagecounter++;
            $_POST["imagecounter"] = $imagecounter;
            imagepng($img, $savefilename);
            imagepng($img, $newfilename);
            $_SESSION['img_file_name'] = $newfilename;

        }
        if($origFeedback == 1){
            if(isset($_SESSION['old_file'.$ansTr])){    
                $oldFile=$_SESSION['old_file'.$ansTr];
            }
            if(isset($_SESSION['img_file_name'])){
                $newfilename = $_SESSION['img_file_name'];
            }	
        }
        // Free up me
        imagedestroy($img);    
        //  }

        if($howSucc==5 || $howSucc==6  || $howSucc==7 || $feedback==1 && $trial%2==0 && $howSucc>=8){
            echo "<img src='$newfilename'>";
        }
        $flag="no";
    }

    ?>
    </td>
    <td width="5%"  >

    </td>

    <td align="left" width="17%"   rowspan="2">
    <div class="previousTrialWin">
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><center><p><b><font color="yellow"> previous  trial</font></b></p></center>
    <table border="1" bordercolor="yellow" align="center" width="140px" height="155px">

    <tr>
    <td align="center">
    <br>

    <?php 

    if($_POST && $origtrial>1){           
        echo "<img width='90px' height='90px' src=$oldFile>";

    }?>
    <font color="yellow">

    <?php 
    if($howSucc==5 && $flagst7==1){
    }

    if($newprevstringColorDom==$newstringColor){?>
        <?php $correctAns="'left'";

    }
    if($newprevstringColorDom!=$newstringColor){
        $correctAns="'right'";

    }?>
    <br>

    <?php 


    if($origtrial>=2){

        if($origFeedback==0){
            if($newprevleftOrRightButton==1){
                //echo str_repeat("&nbsp;", 1); 
                //echo"you answered 'left'";?>
                
                <script>
                $( document ).ready(function() {
                    document.getElementById("myBtnLeft").className="btn btn-success btn-sm";
                });	
                </script>
                <?php }
            if($newprevleftOrRightButton==2){
                //echo str_repeat("&nbsp;", 1); 
                //echo"you answered 'right'";?>
                <script>
                $( document ).ready(function() {
                    document.getElementById("myBtnRight").className="btn btn-success btn-sm";
                });		
                </script>
                <?php 	}
        }
        else{
            if ($number==1){   
                //echo "<p>&nbsp;"; 
                //echo " you answered 'left'"; ?>
                <script>
                $( document ).ready(function() {
                    document.getElementById("myBtnLeft").className="btn btn-success btn-sm";
                });	
                </script>
                <?php }
            if ($number==2){    
                //	echo "<p>&nbsp;";  
                //echo " you answered 'right'";?>
                <script>
                $( document ).ready(function() {
                    document.getElementById("myBtnRight").className="btn btn-success btn-sm";
                });				
                </script>
                <?php
            }
        }
        if($_POST){?>
            <button  id="myBtnLeft" type="button"  class="btn  btn-sm" ><br></button>&nbsp;&nbsp;&nbsp;&nbsp;
            <button id="myBtnRight" type="button"  class="btn btn-sm" >&nbsp;</button>

            <?php }?>





        

        <?php 	if(($howSucc<=5)  || ($howSucc>=6 && $trial % 2 == 0) || ($howSucc>=6 && $origtrial % 2 == 0 && $origFeedback==1)){
            ?>
            
            
            
            
            

            <?php	
            echo"<br>";
            if(($origFeedback==0 && $howSucc<=6)  || ($origFeedback==0 && $howSucc>=7 && $trial % 2 == 0)){
                
                //echo "<br>";
                //echo "correct answer ".$correctAns;
            }if(($origFeedback==1 && $howSucc<=6) || ($origFeedback==1 && $howSucc>=7 && $trial % 2 == 1)){
                //echo "<br>";
                //echo "correct answer ".$correct;
            }?>
            </font>
            
            
            <?php }
        echo "<br>";
        if((($howSucc<=5) || ($howSucc>=6 && $trial % 2 == 0)) && $origFeedback==0){
            if(($newprevstringColorDom==$newstringColor && $newprevleftOrRightButton=='1') ||($newprevstringColorDom!=$newstringColor && $newprevleftOrRightButton=='2')){
                echo"<img src='smiley.jpeg' width='30px' height='30'>";
                $prevSmiley = "happy";
            }if(($newprevstringColorDom==$newstringColor && $newprevleftOrRightButton=='2') ||($newprevstringColorDom!=$newstringColor && $newprevleftOrRightButton=='1')){
                echo"<img src='sadsmiliey2.jpeg' width='30px' height='30'>";
                $prevSmiley = "sad";
            }
        }
        if(($origFeedback==1 && $trial>2 && $howSucc<=5) || ($howSucc>=6 && $origtrial % 2 == 0 && $origFeedback==1)) {
            if($prevSmiley == "sad"){
                echo"<img src='sadsmiliey2.jpeg' width='30px' height='30'>";
            }else{
                echo"<img src='smiley.jpeg' width='30px' height='30'>";
            }
        }
        
    }
    ?>
    </div>
    </td>
    </tr>
    </table>
    </td>
    <td width="18%" >
    </td>
    </tr>
    <tr>
    <td width="13%"  height="170px">
    </td>
    <td width="18%"  ">
</td>


    <?php if((!$_POST || $feedback==1)&&($howSucc<=6)){?>
            
    <TD width="29%"  align="center"> <table width="220px" height="240px" border="3px" bordercolor="yellow"><tr valign="top" align="center"><td>
        
    <?php }else{?>
    <td width="29%"  align="center"><table width="220px" height="240px" border="3px"  bordercolor="yellow"><tr valign="top" align="center"><td id="mydiv3">	
    <?php }
    if(!$_POST || $feedback==1){
        ?>
        <br><p><b><font color="yellow">please select one button</font></b></p>
        <canvas id="circle" width="200" height="30"></canvas>


<?php }else{?>
    <br><b><font color="yellow">please select one button</font></b></p>
        <canvas id="circle" width="200" height="30"></canvas>

    <?php } if($trialPart2<31 && $origFeedback==0 || $trialPart2==31 && $origFeedback==0){
    $action=$_SERVER['PHP_SELF']; 
    }if($trialPart2==31 && $origFeedback==1){
    $action="feedback.php";

    }	
    //action="<?php echo $action;
    ?>

    
    
    <form id="myForm" name="input"  action="<?php echo $action;?>" method="post">
    <input type="hidden"  name="hidden" value="<?php echo $trial;?>">
    <input type="hidden"  name="hiddenStrColorDom" value="<?php echo $stringColorDom;?>">
    <input type="hidden"  name="hiddenCounterLenArray" value="<?php echo $counterLenArray;?>">
    <input type="hidden"  name="hiddenTrialPart2" value="<?php echo $trialPart2;?>">
    <input type="hidden"  name="hiddenStrColor" value="<?php echo $stringColor;?>">
    <input type="hidden"  name="hiddenCountPositive" value="<?php echo $countPositive;?>">
    <input type="hidden"  name="hiddensucsses" value="<?php echo $sucsses;?>">
    <input type="hidden"  name="hiddenHowSuccess" value="<?php echo $howSucc;?>">
    <input type="hidden"  name="imagecounter" value="<?php echo $imagecounter;?>">
    <input type="hidden"  name="numRound" value="<?php echo $numRound;?>">
    <input type="hidden"  name="hiddenFlag" value="<?php echo $flag;?>">
    <input type="hidden"  name="hiddenColorCircle" value="<?php echo $color;?>">
    <input type="hidden"  name="hiddenFeedback" value="<?php echo $feedback;?>">
    <input type="hidden"  name="hiddenNumberCircles" value="<?php echo $num1;?>">
    <input type="hidden"  name="hiddenNumberDomCircles" value="<?php echo $numDomCircles;?>">
    <input type="hidden"  name="hiddenNumber2ColorsCircles" value="<?php echo $numColor2Circles;?>">
    <input type="hidden"  name="hiddenTrialEvenFeedbacks" value="<?php echo $trialEvenFeedbacks;?>">
    <input type="hidden"  name="hiddenPrevleftOrRightButton" value="<?php echo $prevleftOrRightButton;?>">
    <input type="hidden"  name="hiddenPrevstringColorDom" value="<?php echo $prevstringColorDom;?>">
    <input type="hidden"  name="hiddennewstringColor" value="<?php echo $prevstringColor;?>">
    <input type="hidden"  name="hiddenCounter2" value="<?php echo $counter2;?>">
    <input type="hidden"  name="hiddenprevnumberDom" value="<?php echo $numberDom;?>">
    <input type="hidden"  name="hiddennumberDom" value="<?php echo $prevnumberDom;?>">
    <input type="hidden"  name="hiddennumber1" value="<?php echo $number1;?>">
    <input type="hidden"  name="hiddenprevnumber1" value="<?php echo $prevsNumber1;?>">
    <input type="hidden"  name="hiddenFlagst7" value="<?php echo $flagst7;?>">
    <input type="hidden"  name="hiddenprevFlagst7" value="<?php echo $prevorigflagst7;?>">
    <input type="hidden"  name="hiddenprevSmiley" value="<?php echo $prevSmiley ?>">
    <input type="hidden"  name="hiddentrialToTable" value="<?php echo $trialToTable ?>">
    <input type="hidden"  name="hiddenCounterMajority" value="<?php echo $counterMajority;?>">
    <input type="hidden"  name="hiddenCounterMinority" value="<?php echo $counterMinority;?>">
    <input type="hidden"  name="hiddenCounterMajorityPart2" value="<?php echo $counterMajorityPart2;?>">
    <input type="hidden"  name="hiddenCounterMinorityPart2" value="<?php echo $counterMinorityPart2;?>">
    <input type="hidden"  name="hiddenCounter9" value="<?php echo $counter9;?>">
    <input type="hidden"  name="hiddenCount" value="<?php echo $count;?>">
    <input type="hidden"  name="hiddenCount1" value="<?php echo $count1;?>">
    <input type="hidden"  name="hiddenCounter9_0" value="<?php echo $counter9_0;?>">
    <input type="hidden"  name="hiddenCounter9_1" value="<?php echo $counter9_1;?>">
    <input type="hidden"  name="hiddenCounter9_2" value="<?php echo $counter9_2;?>">
    <input type="hidden"  name="hiddenCounter9_3" value="<?php echo $counter9_3;?>">
    <input type="hidden"  name="hiddenCounter9_4" value="<?php echo $counter9_4;?>">
    <input type="hidden"  name="hiddenCounter9_5" value="<?php echo $counter9_5;?>">
    <input type="hidden"  name="hiddenhowManyParamColor2" value="<?php echo $howManyParamColor2;?>">
    <input type="hidden"  name="hiddenhowManyParamColorDom" value="<?php echo $howManyParamColorDom;?>">
    
    


    <?php if($trial>=2){?>	
        <input type="hidden"  name="hiddenYourAnswer" value="<?php echo $newprevleftOrRightButton ?>">
        <input type="hidden"  name="hiddenCorrectAnsw" value="<?php echo $correctAns ?>">
        <?php }?>


    <input type="hidden"  name="hiddenCounter" value="<?php echo $counter;?>">
    <?php if(!$_POST || $feedback==1){?>
        <input type="hidden"  name="hiddenTime" value="<?php echo $timer;?>">
        <button type="submit" name="whichButtonPressed" value="1" class="btn  btn-default" >&nbsp;&nbsp;&nbsp;</button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <button type="submit" name="whichButtonPressed" value="2" class="btn btn-default ">&nbsp;&nbsp;&nbsp;</button>
        <?php }else{?>
        <input type="hidden"  name="hiddenprevTime" value="<?php echo $prevtime;?>">
        <?php if($leftOrRightButton==1){?>
            <button disabled  type="button"  value="1" class="btn btn-success" >&nbsp;&nbsp;&nbsp;</button>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <button type="button"  value="2" class="btn btn-default ">&nbsp;&nbsp;&nbsp;</button>
            <?php }else{?>
            <button  type="button"  value="1" class="btn  btn-default" >&nbsp;&nbsp;&nbsp;</button>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <button disabled type="button"  value="2" class="btn btn-success ">&nbsp;&nbsp;&nbsp;</button>

            <?php }?>
        <?php }
    ?>
    </form>
    <script>
            
            var timer=setTimeout(clickAutoButton,0);
            
            function clickAutoButton(){
                var myForm=document.getElementById("myForm");
                myForm.submit(); 
                myStopFunction();
            }
            function myStopFunction(){
                clearTimeout(timer);
            }
            
            </script>  

    <?php }
//function cheeck if coordinate exist. If it is, then search other coordinate
function checkIfCoord($xCoord,$yCoord,$counterLenArray,$coordArray){
    for ($index=0;$index<$counterLenArray;){

        if($xCoord==$coordArray[$index] && $yCoord==$coordArray[$index+1])
        {
            $xCoord=round(mt_rand(2,6))*63+30;
            $yCoord=round(mt_rand(2,6))*63+30;
            return checkIfCoord($xCoord,$yCoord,$counterLenArray,$coordArray);

        }else{
            $index=$index+2;
        }
    }
    $newxCoord=$xCoord;
    $newyCoord=$yCoord;
    return array($newxCoord,$newyCoord);


}

//trials with 7 circles 1 circle one color and 6 same color circles

function threeCircles($count,$count1){
    //$count=0;
    //$count1=0;
    $num1=5;
    $number=round(mt_rand(1.1,2.98),PHP_ROUND_HALF_DOWN);
    //TODO
    
    if($number==2){
        $count++;
        $number2=2;
        $number=3;
        $numberDom=$number;
        $numberLess=$number2;
    }else{
        $count1++;
        $number2=3;
        $number=2;
        $numberDom=$number2;
        $numberLess=$number;
    }
    
    return array($num1,$numberDom,$numberLess);
}


//trials with 7 circles 1 circle one color and 6 same color circles
function threeOtherCircles(){
    $num1=5;
    $number=mt_rand(2,3);
    $number2=$num1-$number;
    if($number>$number2){
        $numberDom=$number;
        $numberLess=$number2;
    }else{
        $numberDom=$number2;
        $numberLess=$number;
    }
    return array($num1,$numberDom,$numberLess);
}

function stage4IncreaseMax(){
    $num=round(mt_rand(6.1,13.98),PHP_ROUND_HALF_DOWN);
    $num1=$num;
    $number=round(mt_rand(1.1,2.98),PHP_ROUND_HALF_DOWN);
    if($number==1){
        $numberDom=$num1-2;
        $numberLess=2;
    }else{
        $numberDom=2;
        $numberLess=$num1-2;
    }
    //echo $numberDom;
    //echo $numberLess;
    return array($num1,$numberDom,$numberLess);
}

function stage5IncreaseMaxAndMin(){
    $numAllCircles=round(mt_rand(7.1,13.98),PHP_ROUND_HALF_DOWN);
    $minCirc= (int)(($numAllCircles-1)/2);
    $minCirc=$minCirc+0.98;
    $numMinCirc=round(mt_rand(3.1,$minCirc),PHP_ROUND_HALF_DOWN);
    $numMaxCirc=$numAllCircles-$numMinCirc;
    
    $numberDom=$numMaxCirc;
    $numberLess=$numMinCirc;


    return array($numAllCircles,$numberDom,$numberLess);
}



function stage6and7_3colors(){
    $numAllCircles=round(mt_rand(11.1,13.98),PHP_ROUND_HALF_DOWN);	
    //$minCirc=2;
    //$minCirc=$minCirc+0.98;
    $numMinCirc=2;
    //if($numMinCirc==2 && ($numAllCircles==9 || $numAllCircles==10)){
    $numMidCirc=3;
    //} 
    //if($numMinCirc==2 && ($numAllCircles==11 || $numAllCircles==12)){
    //	$numMidCirc=round(mt_rand(3.1,4.98),PHP_ROUND_HALF_DOWN);
    //}
    //if($numMinCirc==2 && $numAllCircles==13){
    //	$numMidCirc=round(mt_rand(3.1,5.98),PHP_ROUND_HALF_DOWN);
    //}
    //if($numMinCirc==3 && ($numAllCircles==12 || $numAllCircles==13)){
    //$numMidCirc=4;
    //}
    $numMaxCirc=$numAllCircles-$numMidCirc-$numMinCirc;
    //}

    //}
    return array($numAllCircles,$numMaxCirc,$numMidCirc,$numMinCirc);

}

function giveFeedback($stringColorDom,$stringColor,$countPositive,$sucsses,$leftOrRightButton,$trial,$trialEvenFeedbacks,$howSucc,$trialPart2,$numberDom,$number1,$flagst7){
    //echo "lorRButton".$leftOrRightButton;

    //positive feedback
    if($howSucc<=8){
        if($stringColorDom==$stringColor && $leftOrRightButton=='1'){
            //echo "<br>";
            //echo "one Sucseed";
            $countPositive=$countPositive+1;
            $sucsses="yes";
            if($howSucc<=5 || ($howSucc>=6 && $trial % 2 == 0) || $trial==1){
                ?>
                <script>
                function DoLoad(){
                    var div=document.createElement("div");

                    document.getElementById("mydiv3").appendChild(div);

                    div.innerHTML="<img src='smiley.jpeg' id='smiley_img' width='100'>";

                    setTimeout(hideimage,1600);
                }
                function hideimage() {
                    document.getElementById('smiley_img').style.display = 'none';
                }
                </script>
                <?php 	}
        }
        //negetive feedback
        if($stringColorDom==$stringColor && $leftOrRightButton=='2'){
            //echo "<br>";
            //echo "lorRButton".$leftOrRightButton;
            //echo "<br>";
            //echo $stringColor;
            //echo "<br>";
            //echo $stringColorDom;
            //echo "<br>";
            //	echo "two noSucseed";
            $countPositive=0;
            if ($howSucc<2){
                $sucsses="no";
            }else{
                $sucsses="yes";
            }
            if($howSucc<=5  || ($howSucc>=6 && $trial % 2 == 0) || ($trial==1)){
                ?>
                <script>
                function DoLoad(){
                    var div=document.createElement("div");
                    document.getElementById("mydiv3").appendChild(div);
                    div.innerHTML="<img src='sadsmiliey2.jpeg' id='sad_smiley_img' width='100'>";
                    setTimeout(hideimage,1600);
                }
                function hideimage() {
                    document.getElementById('sad_smiley_img').style.display = 'none';
                }
                </script>
                <?php }

        }

        //negetive feedback
        if($stringColorDom != $stringColor && $leftOrRightButton=='1'){
            //echo "<br>";
            //echo "lorRButton".$leftOrRightButton;
            //echo "one noSucseed";
            $countPositive=0;
            if ($howSucc<2){
                $sucsses="no";
            }else{
                $sucsses="yes";
            }
            if($howSucc<=5  || ($howSucc>=6 && $trial % 2 == 0) || ($trial==1)){
                ?>
                <script>
                function DoLoad(){
                    var div=document.createElement("div");
                    document.getElementById("mydiv3").appendChild(div);
                    div.innerHTML="<img src='sadsmiliey2.jpeg' id='sad_smiley_img' width='100' >";
                    setTimeout(hideimage,1600);
                }
                function hideimage() {
                    document.getElementById('sad_smiley_img').style.display = 'none';
                }

                </script>
                <?php }
        }
        //positive feedback
        if($stringColorDom != $stringColor && $leftOrRightButton=='2'){
            //echo "<br>";
            //echo "lorRButton".$leftOrRightButton;
            //echo "two sucseed";
            $countPositive=$countPositive+1;
            $sucsses="yes";
            if($howSucc<=5 || ($howSucc>=6 && $trial % 2 == 0) || ($trial==1)){
                ?>
                <script>
                function DoLoad(){
                    var div=document.createElement("div");
                    document.getElementById("mydiv3").appendChild(div);
                    div.innerHTML="<img src='smiley.jpeg' id='smiley_img' width='100'>";
                    setTimeout(hideimage,1600);
                }
                function hideimage() {
                    document.getElementById('smiley_img').style.display = 'none';
                }

                </script>
                <?php }
        }
        
    }
    return array($countPositive,$sucsses);	
}

//now following trials with only even feedback

//part 2.The Experimrnt!!! 
//One trial we draw 11 circles- 2,3,6 and the next time we draw 11 circles - 2,4,5; alternately.
//Three colors. Only 11 circles. Center circle color is determined by parameter $colorChosen. if $colorChosen=1 then the color will be  the color of the Dom circles
//$colorChosen=2; center circle color=color2; $colorChosen=3 center circle color=color3

function stage8_3colors($counter9,$counter9_0,$counter9_1,$counter9_2,$counter9_3,$counter9_4,$counter9_5,$numRound){
    $array=array();
    $array1_3=array(1,3);
    $num1=13;
    //non-ambiguous
    if($numRound==1){
        $numberDom=7;
        $number1=4;
        $number2=2;
        $colorChosen=1;
        $counter9++;
        $counter9_3++;
    }    
    if($numRound==2){
        $numberDom=7;
        $number1=4;
        $number2=2;
        $colorChosen=3;
        $counter9++;
        $counter9_5++;
    }if($numRound==3){
        $numberDom=6;
        $number1=4;
        $number2=3;
        $colorChosen=3;
        $counter9++;
        $counter9_4++;
    }
    
    //ambiguous
    if($numRound==4){
        //echo "3,4,6,color1";
        $numberDom=6;
        $number1=4;
        $number2=3;
        $colorChosen=1;
        $counter9++;
        $counter9_2++;
    }    
    if($numRound==5){
        //echo "6,4,3,color2";
        $numberDom=6;
        $number1=4;
        $number2=3;
        $colorChosen=2;
        $counter9++;
        $counter9_0++;			
    } 
    
    if($numRound==6){
        //echo "2,4,7,color2";
        $numberDom=7;
        $number1=4;
        $number2=2;
        $colorChosen=2;
        $counter9++;
        $counter9_1++;
        
    }
    
    return array($num1,$numberDom,$number1,$number2,$colorChosen,$counter9,$counter9_0,$counter9_1,$counter9_2,$counter9_3,$counter9_4,$counter9_5);
}



if (!$_POST){
    $result1="INSERT INTO 2colorsJonRing(ID, numberOfTrail,colordom,howManyCircles,howManyDomminanteColorCircles, howManyLessCircles,stringColorDom,StringColor2,whichColorCenterCircle,WhichButtonPressedPerviousTrial,time ,date) VALUES('$ses_id',1,'$stringColorDom','$num1','$numDomCircles','$numColor2Circles','$stringColorDom','$stringColor2','$stringColor', 0,'$timer',NOW())";
    //mysql_query($result1,$link);
}
if($howSucc<5 && $trial>1 && $origFeedback==0 ){
    $result="INSERT INTO 2colorsJonRing(ID,numberOfTrail,colordom,howManyCircles,howManyDomminanteColorCircles,howManyLessCircles,stringColorDom,StringColor2,whichColorCenterCircle, WhichButtonPressedPerviousTrial,time,date) VALUES('$ses_id','$trial','$stringColorDom',$num1,'$numDomCircles','$numColor2Circles','$stringColorDom','$stringColor2','$stringColor', '$newprevleftOrRightButton','$time',NOW())";
    //mysql_query($result, $link);
    //  echo " successfully\n";
    // } else {
    //    echo 'Error insert: ' . mysql_error() . "\n";
    //  }
    
    
}
if($howSucc>=5 && $origFeedback==0){
    $resultPart2= "INSERT INTO 3colorsJonRing(ID, numberOfTrail,colordom,color2,color3,howManyCircles,howManyDomminanteCircles,howManyCircles1,howManyCircles2,whichColorCenterCircle,WhichButtonPressedPerviousTrial,time,date) VALUES('$ses_id','$trial','$stringColorDom','$stringColor2','$stringColor3','$num1','$numberDom','$number1','$number2','$stringColor','$newprevleftOrRightButton','$time',NOW())";

}
//mysql_close($link);
?>
</td></tr></table></TD>

<?php if(!$_POST || $feedback==1){?>

    <td  width="5%"  valign="top" align="center">
    </td>
    <?php }else{?>
    <td width="5%"   id="mydiv3" valign="top" align="center"></td>                                                                
    <?php }?>
<td width="15%" >

</td>
<td width="20%" >

</td>



</TR>
</TABLE>



</div>

</html>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
