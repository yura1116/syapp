package com.example.syapp.ui.home;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.example.syapp.R;
import com.example.syapp.databinding.FragmentHomeBinding;

public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;
    private Button home_syyy_btn;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        HomeViewModel homeViewModel =
                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        return root;
    }

    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        home_syyy_btn = getActivity().findViewById(R.id.home_syyy);
        home_syyy_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.out.println("点击适用语言按钮");

                // 初始化Python解释器
                if (!Python.isStarted()) {
                    Python.start(new AndroidPlatform(getActivity()));
                }
                // 导入Python模块
                Python python = Python.getInstance();
                PyObject pyModule = python.getModule("test_around_db");

                // 调用Python函数
                PyObject result = pyModule.callAttr("test_around_db");

                // 处理Python函数的返回值
                String pythonResult = result.toJava(String.class);
                System.out.println(pythonResult);
            }
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}