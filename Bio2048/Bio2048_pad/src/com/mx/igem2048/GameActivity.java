package com.mx.igem2048;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.DialogInterface.OnClickListener;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.mx.igem2048.view.Layout2048;
import com.mx.igem2048.view.Layout2048.OnGame2048Listener;

public class GameActivity extends Activity implements OnGame2048Listener,android.view.View.OnClickListener
{
	private Layout2048 mGame2048Layout;
	private TextView mScore;
	private TextView bScore;
	private int mColumn_s;//表示棋盘类型
	private int history;//表示历史分数
	private int bRank = 0;//表示当前最大等级
	private ImageButton study;
	private int flag;//标志study按钮的情况	
	
	private static int[] mImgs = new int[] { R.drawable.p1, R.drawable.p2,
		R.drawable.p3, R.drawable.p4, R.drawable.p5, R.drawable.p6,
		R.drawable.p7, R.drawable.p8, R.drawable.p9, R.drawable.p10,R.drawable.p11,
		R.drawable.p12,R.drawable.p13 };
	
	private static String[] mstr = new String[]{"ATGC","DNA","protein","organelle","cell",
			"tissue","organ","system","individual","population",
			"community","ecosystem","biosphere"};

	
	@Override
	protected void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_game);
						
		mScore = (TextView) findViewById(R.id.score);		
		bScore = (TextView) findViewById(R.id.best);
		
		study = (ImageButton)findViewById(R.id.study);
		study.setOnClickListener(this);
		
		//绑定滑动的layout
		mGame2048Layout = (Layout2048) findViewById(R.id.id_game2048);
		mGame2048Layout.setOnGame2048Listener(this);
				
		//取出模式的数据
		SharedPreferences mSharedPreferences = getSharedPreferences("My", 0);
		mColumn_s = mSharedPreferences.getInt("pattern", 4);
		
		//设置棋盘模式
		mGame2048Layout.setmColumn(mColumn_s);
		
		//读取学习模式标志，并设置
		flag = mSharedPreferences.getInt("study", 1);
		if(flag==1)
			study.setImageResource(R.drawable.bt_study);
		else
			study.setImageResource(R.drawable.bt_unstudy);
		
		
		//取出历史值
		switch(mColumn_s){
		case 5:
			history = mSharedPreferences.getInt("bscore5", 0);
			break;
		default:
			history = mSharedPreferences.getInt("bscore4", 0);
			break;
		}
		
		//change bscore when initial activity
		bScore.setText(""+history);
	}
	
	/*
     * 从布局文件中加载布局并且自定义显示Toast
     */
    public void showCustomToast(int rank){
        //获取LayoutInflater对象，该对象可以将布局文件转换成与之一致的view对象
        LayoutInflater inflater=getLayoutInflater();
        //将布局文件转换成相应的View对象
        View layout=inflater.inflate(R.layout.activity_toast,(ViewGroup)findViewById(R.id.toast_layout_root));
        
        //从layout中按照id查找imageView对象
        ImageView imageView=(ImageView)layout.findViewById(R.id.ivForToast);
        //设置ImageView的图片
        imageView.setBackgroundResource(mImgs[rank-1]);
        
        //从layout中按照id查找TextView对象
        TextView textView=(TextView)layout.findViewById(R.id.tvForToast);
        //设置TextView的text内容
        textView.setText(mstr[rank-1]);
        
        //实例化一个Toast对象
        Toast toast=new Toast(getApplicationContext());
        toast.setDuration(Toast.LENGTH_SHORT);
        toast.setView(layout);
        toast.show();
    }

	
    @Override
    public void onRankChange(){
    	
    	if(flag==1){
    		if(bRank < mGame2048Layout.getHighestRank())  		
			{
    			bRank = mGame2048Layout.getHighestRank();
    			showCustomToast(bRank);
			}
    	}
    }
    
	@Override
	public void onScoreChange(int score)
	{
		int score_num;
		int bscore_num;
		
		SharedPreferences mSharedPreferences = getSharedPreferences("My", 0);
		SharedPreferences.Editor mEditor = mSharedPreferences.edit();
		
		//change score
		mScore.setText(""+score);		
		
		score_num = score;
		
		if(history<score_num)
			{
				//change bscore
				bScore.setText(""+score_num);
				
				//save bscore
				bscore_num = score_num;
				switch(mColumn_s){
				case 5:
					mEditor.putInt("bscore5", bscore_num);
					break;
				default:
					mEditor.putInt("bscore4", bscore_num);
					break;
				}												
				mEditor.commit();
			}			
	}
	
	

	
	@Override
	public void onGameOver()
	{				
		new AlertDialog.Builder(this).setTitle("GAME OVER")
				.setMessage("YOU HAVE GOT " + mScore.getText())
				.setPositiveButton("RESTART", new OnClickListener()
				{
					@Override
					public void onClick(DialogInterface dialog, int which)
					{
						mGame2048Layout.restart();
					}
				}).setNegativeButton("EXIT", new OnClickListener()
				{

					@Override
					public void onClick(DialogInterface dialog, int which)
					{
						Intent intent = new Intent();
						intent.setClass(GameActivity.this,MainActivity.class);
						finish();
						startActivity(intent);
					}
				}).show();
			
	}
	
	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
        	Intent intent = new Intent();
    		intent.setClass(GameActivity.this,MainActivity.class);
    		startActivity(intent);
		    finish();
            return false;
        }
        return super.onKeyDown(keyCode, event);
    }

	
	@Override
	public void onClick(View v) {
		// TODO Auto-generated method stub
		
		SharedPreferences mSharedPreferences = getSharedPreferences("My", 0);
		SharedPreferences.Editor mEditor = mSharedPreferences.edit();
		Toast toast;
		
		flag = mSharedPreferences.getInt("study", 1);	
		
		if(flag==1)
		{
			study.setImageResource(R.drawable.bt_unstudy);
			flag = 0;
			mEditor.putInt("study", flag);
			mEditor.commit();
			toast = Toast.makeText(this,"Quit learning mode", Toast.LENGTH_SHORT);
     	    toast.show();
		}
		else
		{
			study.setImageResource(R.drawable.bt_study);
			flag = 1;
			mEditor.putInt("study", flag);
			mEditor.commit();
			toast = Toast.makeText(this,"select learning mode", Toast.LENGTH_SHORT);
     	    toast.show();
		}					
		
	}

}
