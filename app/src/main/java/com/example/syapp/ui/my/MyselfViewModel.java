package com.example.syapp.ui.my;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class  MyselfViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public MyselfViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("这是我的页面");
    }

    public LiveData<String> getText() {
        return mText;
    }
}