package com.example.syapp.ui.my;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.syapp.databinding.FragmentMyselfBinding;

public class MyselfFragment extends Fragment {


    private FragmentMyselfBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        MyselfViewModel myselfViewModel =
                new ViewModelProvider(this).get(MyselfViewModel.class);

        binding = FragmentMyselfBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        /*final TextView textView = binding.textMyself;
        myselfViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);*/
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}