package com.example.syapp.ui.shiting;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class ShitingViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public ShitingViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("这是试听声音");
    }

    public LiveData<String> getText() {
        return mText;
    }
}