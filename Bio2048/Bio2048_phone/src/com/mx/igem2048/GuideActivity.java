package com.mx.igem2048;

import java.util.Timer;
import java.util.TimerTask;

import com.mx.igem2048.R;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageButton;
import android.widget.Toast;

public class GuideActivity extends Activity implements OnClickListener{
	
    private ImageButton next; 
    private int flag = 0;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
    	
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_guide);
        
        final Intent intent = new Intent();
        Timer timer = new Timer();
        TimerTask task = new TimerTask(){

			@Override
			public void run() {
				// TODO Auto-generated method stub
				intent.setClass(GuideActivity.this,MainActivity.class);
				if(flag == 0)
					{
						GuideActivity.this.startActivity(intent);
						finish();
					}
			}};
        timer.schedule(task, 1000*3);	  
        
        next =(ImageButton)this.findViewById(R.id.next);
        next.setOnClickListener(this);
       
    }

	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		Intent intent = new Intent();
		intent.setClass(GuideActivity.this,MainActivity.class);
		
		switch (v.getId()) {
		   case R.id.next:
		       startActivity(intent);
		       flag = 1;
		       finish();
			   break;
	    }
	}
}