package com.helloworld;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


@SpringBootApplication
public class Application {
    public static void main(String[] args) throws IOException, InterruptedException {
        SpringApplication.run(Application.class, args);

        seperateData();

    }


    public static void seperateData() throws IOException, InterruptedException {

        System.out.println("i am here");
        String pyFile = "/Users/liujun/helloWorld/src/main/python/seperateRaw.py";
        String file = "/Users/liujun/helloWorld/src/main/resources/static/files/1.xlsx988644680805823565.xlsx";
        String output = "/Users/liujun/helloWorld/src/main/resources/static/files/";
        String[] pythonData =new String[]{"python", pyFile, file, output};

        Process pr = Runtime.getRuntime().exec(pythonData);

        BufferedReader in = new BufferedReader(new InputStreamReader(
                pr.getInputStream()));
        String line;
        while ((line = in.readLine()) != null) {
            System.out.println(line);
        }
        in.close();
        pr.waitFor();
        System.out.println("end");

    }

}
