package com.mx.igem2048;

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.view.ViewPager;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

public class RuleActivity extends Activity {  
    
	private List<View>viewList;
	private ViewPager pager;
	private int appear_flag;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
    	
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rule);
        
        viewList = new ArrayList<View>();
        
        //View对象作为ViewPager数据源
        View view1 = View.inflate(this, R.layout.activity_ruleone, null);
        View view2 = View.inflate(this, R.layout.activity_ruletwo, null);
        View view3 = View.inflate(this, R.layout.activity_rulethree, null);
        View view4 = View.inflate(this, R.layout.activity_rulefour, null);
        View view5 = View.inflate(this, R.layout.activity_rulefive, null);
                
        viewList.add(view1);
        viewList.add(view2);
        viewList.add(view3);
        viewList.add(view4);
        viewList.add(view5);
        
       //初始化ViewPager
       pager = (ViewPager)findViewById(R.id.pager);
        
       //创建PagerAdapter的适配器
       MyPagerAdapter adapter = new MyPagerAdapter(viewList);
        
       //ViewPager加载适配器
       pager.setAdapter(adapter);
       
       SharedPreferences msharedPreferences = getSharedPreferences("My",0);
       SharedPreferences.Editor mEditor = msharedPreferences.edit();
       
       appear_flag = msharedPreferences.getInt("appear_", 0);
       if(appear_flag==0)
    	   {
    	   		showCustomToast();
    	   		mEditor.putInt("appear_", 1);
    	   		mEditor.commit();
    	   }
        
    } 
    
    public void showCustomToast(){
        //获取LayoutInflater对象，该对象可以将布局文件转换成与之一致的view对象
        LayoutInflater inflater=getLayoutInflater();
        //将布局文件转换成相应的View对象
        View layout=inflater.inflate(R.layout.toast_rule,
        		(ViewGroup)findViewById(R.id.toast_rule));
        
        //实例化一个Toast对象
        Toast toast=new Toast(getApplicationContext());
        toast.setDuration(Toast.LENGTH_SHORT);
        toast.setView(layout);
        toast.show();
    }
    
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
        	Intent intent = new Intent();
    		intent.setClass(RuleActivity.this,MainActivity.class);
    		startActivity(intent);
		    finish();
            return false;
        }
        return super.onKeyDown(keyCode, event);
    }
}
