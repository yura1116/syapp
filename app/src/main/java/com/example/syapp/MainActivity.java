package com.example.syapp;

import android.Manifest;
import android.content.pm.PackageManager;
import android.content.res.AssetManager;
import android.os.Bundle;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.example.syapp.databinding.ActivityMainBinding;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends AppCompatActivity {

    private ActivityMainBinding binding;
    private static final int CAMERA_PERMISSION_REQUEST_CODE = 100;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        BottomNavigationView navView = findViewById(R.id.nav_view);

        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_peixing, R.id.navigation_shiting,R.id.navigation_myself)
                .build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_activity_main);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(binding.navView, navController);

        // 检查是否有相机权限，如果没有，请求权限
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, CAMERA_PERMISSION_REQUEST_CODE);
        } else {
            // 如果已经拥有相机权限，继续执行您的代码
            //initPythonEnvironment();
        }
    }

    // 初始化 Python 环境
    private void initPythonEnvironment() {
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        Python python = Python.getInstance();

        // 获取 Python 模块
        PyObject pyObject = python.getModule("live_detection");

        // 复制 shape_predictor_68_face_landmarks.dat 文件到应用的私有目录
        copyFileFromAssets("shape_predictor_68_face_landmarks.dat");

        // 调用 Python 函数并传递文件路径
        String filePath = getFilesDir() + File.separator + "shape_predictor_68_face_landmarks.dat";
        pyObject.callAttr("live_detection", filePath);
    }

    private void copyFileFromAssets(String filename) {
        AssetManager assetManager = getAssets();
        try {
            InputStream inputStream = assetManager.open(filename);
            File outputFile = new File(getFilesDir(), filename);
            FileOutputStream outputStream = new FileOutputStream(outputFile);
            byte[] buffer = new byte[1024];
            int length;
            while ((length = inputStream.read(buffer)) > 0) {
                outputStream.write(buffer, 0, length);
            }
            inputStream.close();
            outputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // 当用户响应权限请求时调用此方法
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        if (requestCode == CAMERA_PERMISSION_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // 用户授予了相机权限，继续执行您的代码
                initPythonEnvironment();
            } else {
                // 用户拒绝了相机权限，您可以向用户解释为什么需要这个权限，或者采取适当的措施
            }
        }

        super.onRequestPermissionsResult(requestCode, permissions, grantResults); // 添加这一行
    }

    // 在某个按钮点击事件中使用相机权限
    public void onCameraButtonClicked(View view) {
        // 检查是否有相机权限
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            // 已经拥有相机权限，可以执行相机相关操作
        } else {
            // 没有相机权限，您可以向用户解释为什么需要这个权限，或者在此处再次请求权限
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, CAMERA_PERMISSION_REQUEST_CODE);
        }
    }
}