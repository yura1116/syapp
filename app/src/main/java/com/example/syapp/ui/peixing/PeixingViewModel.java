package com.example.syapp.ui.peixing;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class PeixingViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public PeixingViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("这是配型页面");
    }

    public LiveData<String> getText() {
        return mText;
    }
}