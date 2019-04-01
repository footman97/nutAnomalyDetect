package com.helloworld.controller;

import org.apache.commons.io.FileUtils;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.InputStream;
import java.util.*;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

@Controller
public class Controllers {

    @ResponseBody
    @RequestMapping(value = "/upload" ,method = RequestMethod.POST)
    public Map<String, Object> uploadFile(HttpServletRequest request,@RequestParam("rawData") MultipartFile[] rawDataFile) throws Exception {

        // 上传文件目录 全路径去掉项目名
        String tempRawFile = "src/main/resources/static/files/tempRaw";
        File dir = new File(tempRawFile);
        if (!dir.exists()){  // 如果目录不存在则创建
            dir.mkdirs();
        }

        InputStream inputStream;

        for (MultipartFile multipartFile : rawDataFile) {
            // 得到文件名
            String filename = multipartFile.getOriginalFilename();
            inputStream = multipartFile.getInputStream();
            // createTempFile生成 文件名+随机数的临时文件，避免冲突
            File tmpFile = File.createTempFile(filename,filename.substring(filename.lastIndexOf(".")),dir);
            FileUtils.copyInputStreamToFile(inputStream, tmpFile);

        }

        // 分离x-y数据
        String seperateDataDir = "src/main/resources/static/files/";
        seperateData(tempRawFile, seperateDataDir, rawDataFile.length);
        //绘图

        //取样
        sampleData(seperateDataDir);

        Map<String, Object> json = new HashMap<String, Object>();
        json.put("message", "文件上传成功");
        return json;

    }

    public void seperateData(String tempRawFile, String seperateDataDir, int fileNums) throws IOException, InterruptedException {

        // 当前路径 /Users/liujun/helloWorld
    //        File directory = new File("");//设定为当前文件夹
    //        System.out.println(directory.getCanonicalPath());//获取标准的路径
    //        System.out.println(directory.getAbsolutePath());//获取绝对路径

        String pSepeCode = "./src/main/python/seperateRaw.py";

        String[] pythonData =new String[]{"python", pSepeCode, tempRawFile, seperateDataDir, fileNums+""};

        Process pr = Runtime.getRuntime().exec(pythonData);
        pr.waitFor();   // 等待进程执行结束
        System.out.println("seperate raw data finished");
//
    }

    public void sampleData(String seperateDataDir) throws IOException, InterruptedException {

        String sampledData = seperateDataDir + "sampleData.xlsx";
        String pSepeCode = "./src/main/python/sampleData.py";
        String xData = seperateDataDir + "xData.xlsx";
        String yData = seperateDataDir + "yData.xlsx";

        File xFile = new File(xData);
        File yFile = new File(yData);
        if (!xFile.exists() || !yFile.exists()){
            System.out.println("seperateData error");
        }
        else{
            String[] pythonData =new String[]{"python", pSepeCode, xData, yData, sampledData};
            Process pr = Runtime.getRuntime().exec(pythonData);
            pr.waitFor();   // 等待进程执行结束
            System.out.println("sample data finished");
        }

    }

    public void

}


//    // for method1(without bootstrap-inputfile)
//    @RequestMapping("/upload")
//    @ResponseBody
//    public String upload(@RequestParam("file") MultipartFile file) {
//        String fileName = file.getOriginalFilename();
//        if(fileName.indexOf("\\") != -1){
//            fileName = fileName.substring(fileName.lastIndexOf("\\"));
//        }
//        String filePath = "src/main/resources/static/files/";
//        File targetFile = new File(filePath);
//        if(!targetFile.exists()){
//            targetFile.mkdirs();
//        }
//        FileOutputStream out = null;
//        try {
//            out = new FileOutputStream(filePath+fileName);
//            out.write(file.getBytes());
//            out.flush();
//            out.close();
//        } catch (Exception e) {
//            e.printStackTrace();
//            return "上传失败";
//        }
//        return "上传成功!";
//    }


//    异步上传方式，注意修改index.html 、 upLoadFile.js文件
//    @ResponseBody
//    @RequestMapping(value = "/upload" ,method = RequestMethod.POST)
//    public Map<String, Object> uploadFile(HttpServletRequest request, HttpServletResponse response) throws Exception {
//
//        request.setCharacterEncoding("UTF-8");
//
//        List<String> rawDataUrl = new ArrayList<>();
//
//        Map<String, Object> json = new HashMap<String, Object>();
//        MultipartHttpServletRequest multipartRequest = (MultipartHttpServletRequest) request;
//
// 上传文件目录 全路径去掉项目名
//        File dir = new File("src/main/resources/static/files");
//        /** 页面控件的文件流* */
//        InputStream inputStream;
//        MultipartFile multipartFile = null;
//        Map map =multipartRequest.getFileMap();
//
//        for (Iterator i = map.keySet().iterator(); i.hasNext();) {
//            Object obj = i.next();
//            multipartFile=(MultipartFile) map.get(obj);
//
//            String filename = multipartFile.getOriginalFilename();
//
////            String rawFilePath = "";
//
//            inputStream = multipartFile.getInputStream();
//            // createTempFile生成 文件名+随机数的临时文件，避免冲突
//            File tmpFile = File.createTempFile(filename,filename.substring(filename.lastIndexOf(".")),dir);
//            FileUtils.copyInputStreamToFile(inputStream, tmpFile);
//            // 记录文件url
//            rawDataUrl.add(tmpFile.getPath());
//            System.out.println(tmpFile.getPath());
//
//        }
//        System.out.println(rawDataUrl.size());
//
//        // 处理数据
////        seperateData(rawFilePath);
////
////        String xData ="./src/main/resources/static/files/xdata1_1.xlsx";
////        String yData ="./src/main/resources/static/files/ydata1_1.xlsx";
////
////        sampleData(xData, yData);
//
//
//
//        json.put("message", "文件上传成功");
////        json.put("path",rawFilePath);
//
//        return json;
//    }

