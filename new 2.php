<?php

  $strAccessToken = "+t5E3u2f0eW3JKhGPyKqGX4M1M6uuvErtuexSZn6D3017/ONS2n+Nqc3KjF37A0K4tv3QZ0BD6kyrzoCXmKa+L2ys817BnmeTwqXPujiaX9+yEpjMBxT2OH60T4W41rZXsUqJ6QidfaesO3AOAb93wdB04t89/1O/w1cDnyilFU=";
  
  $content = file_get_contents('php://input');
  $arrJson = json_decode($content, true);

  $strUrl = "https://api.line.me/v2/bot/message/reply";

  $arrHeader = array();
  $arrHeader[] = "Content-Type: application/json";
  $arrHeader[] = "Authorization: Bearer {$strAccessToken}";
  $_msg = $arrJson['events'][0]['message']['text'];


  $api_key="xX3Bhqg9gp1ds9yfrPfgzaa8BlYS2igP";
  $url = 'https://api.mongolab.com/api/1/databases/data/collections/datas?apiKey='.$api_key.'';
  $json = file_get_contents('https://api.mongolab.com/api/1/databases/data/collections/datas?apiKey='.$api_key.'&q={"question":"'.$_msg.'"}');
  $data = json_decode($json);
  $isData=sizeof($data);

  if (strpos($_msg, 'H.E.L.E.N') !== false) 
  {
    if (strpos($_msg, 'H.E.L.E.N') !== false) 
    {
      $x_tra = str_replace("H.E.L.E.N","", $_msg);
      $pieces = explode("|", $x_tra);
      $_question=str_replace("[","",$pieces[0]);
      $_answer=str_replace("]","",$pieces[1]);
      //Post New Data
      $newData = json_encode(
        array(
          'question' => $_question,
          'answer'=> $_answer
        )
      );
      $opts = array(
        'http' => array(
            'method' => "POST",
            'header' => "Content-type: application/json",
            'content' => $newData
         )
      );
      $context = stream_context_create($opts);
      $returnValue = file_get_contents($url,false,$context);
      $arrPostData = array();
      $arrPostData['replyToken'] = $arrJson['events'][0]['replyToken'];
      $arrPostData['messages'][0]['type'] = "text";
      $arrPostData['messages'][0]['text'] = 'Thank you.';
    }
  }
  else
  {
    if($isData >0){
       foreach($data as $rec){
        $arrPostData = array();
        $arrPostData['replyToken'] = $arrJson['events'][0]['replyToken'];
        $arrPostData['messages'][0]['type'] = "text";
        $arrPostData['messages'][0]['text'] = $rec->answer;
       }
    }
    else
    {
        $arrPostData = array();
        $arrPostData['replyToken'] = $arrJson['events'][0]['replyToken'];
        $arrPostData['messages'][0]['type'] = "text";
        $arrPostData['messages'][0]['text'] = 'H.E.L.E.N คุณสามารถสอนให้ฉันฉลาดได้เพียงพิมพ์: H.E.L.E.N[คำถาม|คำตอบ]';
    }
  }

  $channel = curl_init();
  curl_setopt($channel, CURLOPT_URL,$strUrl);
  curl_setopt($channel, CURLOPT_HEADER, false);
  curl_setopt($channel, CURLOPT_POST, true);
  curl_setopt($channel, CURLOPT_HTTPHEADER, $arrHeader);
  curl_setopt($channel, CURLOPT_POSTFIELDS, json_encode($arrPostData));
  curl_setopt($channel, CURLOPT_RETURNTRANSFER,true);
  curl_setopt($channel, CURLOPT_SSL_VERIFYPEER, false);
  $result = curl_exec($channel);
  curl_close ($channel);
  echo "sucess full";
?>