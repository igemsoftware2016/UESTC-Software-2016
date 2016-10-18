package com.mx.igem2048;

import com.mx.igem2048.R;

import android.animation.ObjectAnimator;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity implements OnClickListener{
    private ImageButton bt_rule;
    private ImageButton bt_pattern; 
    private ImageButton bt_play; 
    private long exitTime = 0;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
    	
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        bt_rule =(ImageButton)this.findViewById(R.id.rule);
        bt_pattern =(ImageButton)this.findViewById(R.id.pattern);
        bt_play =(ImageButton)this.findViewById(R.id.play);
        bt_rule.setOnClickListener(this);
        bt_pattern.setOnClickListener(this);
        bt_play.setOnClickListener(this);
        
       
    }
    
    
	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		Intent intent = new Intent();
		ObjectAnimator animator = ObjectAnimator.ofFloat(v, "alpha", 0F,1F);
		animator.setDuration(500);
		
		switch (v.getId()) {
		   //main1_paly   main2_pattern    main3_rule
		   case R.id.play:
			   animator.start();			
			   
			   intent.setClass(MainActivity.this,GameActivity.class);
		       startActivity(intent);
		       finish();
			   break;
		   case R.id.pattern:
			   animator.start();
			   
			   intent.setClass(MainActivity.this,PatternActivity.class);
		       startActivity(intent);
		       finish();
			   break;
		  case R.id.rule:
			   animator.start();
			   
			   intent.setClass(MainActivity.this,RuleActivity.class);
		       startActivity(intent);
		       finish();
			   break;
	    }
	} 
	
	
	
	//以下是对返回键的操作
	@Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            exit();
            return false;
        }
        return super.onKeyDown(keyCode, event);
    }

    public void exit() {
        if ((System.currentTimeMillis() - exitTime) > 2000) {
            Toast.makeText(getApplicationContext(), "Pressing again will exit program",
                    Toast.LENGTH_SHORT).show();
            exitTime = System.currentTimeMillis();
        } else {
            finish();
            System.exit(0);
        }
    }
}
