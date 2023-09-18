package com.example.syapp.ui.my;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TabHost;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.viewpager.widget.ViewPager;

import com.example.syapp.LoginFragment;
import com.example.syapp.R;
import com.example.syapp.RegFragment;
import com.example.syapp.databinding.FragmentMyselfBinding;
import com.google.android.material.tabs.TabLayout;

public class MyselfFragment extends Fragment {
    private TabLayout tabLayout;
    private ViewPager viewPager;

    private FragmentMyselfBinding binding;
    private TabHost tabHost;
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_myself, container, false);

        tabLayout = rootView.findViewById(R.id.tabLayout);
        viewPager = rootView.findViewById(R.id.viewPager);

        // 创建适配器以管理不同选项卡的内容
        TabPagerAdapter adapter = new TabPagerAdapter(getChildFragmentManager());

        // 添加选项卡（假设您有三个选项卡）
        adapter.addFragment(new LoginFragment(), "登录");
        adapter.addFragment(new RegFragment(), "注册");

        // 设置ViewPager的适配器
        viewPager.setAdapter(adapter);

        // 将TabLayout与ViewPager关联
        tabLayout.setupWithViewPager(viewPager);

        return rootView;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}