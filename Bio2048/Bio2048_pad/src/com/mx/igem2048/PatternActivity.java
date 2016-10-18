package com.mx.igem2048;

import android.animation.ObjectAnimator;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageButton;
import android.widget.Toast;

public class PatternActivity extends Activity implements OnClickListener{
    private ImageButton four;
    private ImageButton five;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
    	
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pattern);
        
        four =(ImageButton)this.findViewById(R.id._4_4);
        five =(ImageButton)this.findViewById(R.id._5_5);
        four.setOnClickListener(this);
        five.setOnClickListener(this);
       
    }   
    
	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		Intent intent = new Intent();
		intent.setClass(PatternActivity.this,MainActivity.class);
		
		Toast toast;
		
		//设置模式参数
		int flag;
		
		
		//设置动画效果
		ObjectAnimator animator = ObjectAnimator.ofFloat(v, "alpha", 0F,1F);
		animator.setDuration(500);
		
		//设置sharedpreference
		SharedPreferences mSharedPreferences = getSharedPreferences("My", 0);
		SharedPreferences.Editor mEditor = mSharedPreferences.edit();
		
		switch (v.getId()) {
		case R.id._4_4:			
			animator.start();
			
			flag = 4;
			//存入值
			mEditor.putInt("pattern", flag);
			mEditor.commit();
			
			//显示toast
			toast = Toast.makeText(this, "have selected 4*4", Toast.LENGTH_SHORT);
     	    toast.show();
     	    
		    startActivity(intent);
		    finish();
			break;
			
        case R.id._5_5:
			animator.start();
        	
			flag = 5;
			//存入值
			mEditor.putInt("pattern", flag);
			mEditor.commit();
			
			//显示toast
			toast = Toast.makeText(this, "have selected 5*5", Toast.LENGTH_SHORT);
     	    toast.show();
     	    
			startActivity(intent);
			finish();
			break;
			
		default:
			break;
		}
	}
	
	public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
        	Intent intent = new Intent();
    		intent.setClass(PatternActivity.this,MainActivity.class);
    		startActivity(intent);
		    finish();
            return false;
        }
        return super.onKeyDown(keyCode, event);
    }
}
