package com.mx.igem2048.view;

import com.mx.igem2048.GameActivity;
import com.mx.igem2048.R;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Paint.Style;
import android.graphics.Rect;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

/**
 * 2048的每个Item
 * 
 * @author zhy
 * 
 */
public class Item2048 extends View
{
	/**
	 * 该View上的数字
	 */
	private int mNumber;
	private String mNumberVal;//用来显示
	private Paint mPaint;
	private int rank;//用来传递rank
	/**
	 * 绘制文字的区域
	 */
	private Rect mBound;
	
	private static int[] mImgs = new int[] { R.drawable.p1, R.drawable.p2,
		R.drawable.p3, R.drawable.p4, R.drawable.p5, R.drawable.p6,
		R.drawable.p7, R.drawable.p8, R.drawable.p9, R.drawable.p10,R.drawable.p11,
		R.drawable.p12,R.drawable.p13 };
	
	private static Bitmap[] mBitmaps = null;
	{
		if (mBitmaps == null)
		{
			mBitmaps = new Bitmap[mImgs.length];
			for (int i = 0; i < mImgs.length; i++)
			{
				mBitmaps[i] = BitmapFactory.decodeResource(getResources(),
						mImgs[i]);
			}

		}

	}

	public Item2048(Context context, AttributeSet attrs, int defStyle)
	{
		super(context, attrs, defStyle);
		mPaint = new Paint();

	}

	public Item2048(Context context)
	{
		this(context, null);
	}

	public Item2048(Context context, AttributeSet attrs)
	{
		this(context, attrs, 0);
	}

	public void setNumber(int number)
	{
		mNumber = number;
		mNumberVal = mNumber + "";
		mPaint.setTextSize(45.0f);
		mBound = new Rect();
		mPaint.getTextBounds(mNumberVal, 0, mNumberVal.length(), mBound);
		/*
		 * 快速获得View的宽度和高度使用Paint.getTextBounds
		 * 得到一个Rect对象
		 */
		invalidate();    
		/*
		 * invalidate()是用来刷新View的，必须是在UI线程中进行工作。比如在修改某
		 * 个view的显示时，调用invalidate()才能看到重新绘制的界面。invalidate()
		 * 的调用是把之前的旧的view从主UI线程队列中pop掉
		 */
	}
	
	

	public int getNumber()
	{
		return mNumber;
	}

	@Override
	protected void onDraw(Canvas canvas)
	{
		
		super.onDraw(canvas);
		String mBgColor = "";
		int index = -1;
		switch (mNumber)
		{
		case 0:
			mBgColor = "#CCC0B3";
			index = 0;
			break;
		case 2:
			mBgColor = "#EEE4DA";
			index = 0;
			rank = 1;
			break;
		case 4:
			mBgColor = "#EDE0C8";
			index = 1;
			rank = 2;
			break;
		case 8:
			mBgColor = "#F2B179";// #F2B179
			index = 2;
			rank = 3;
			break;
		case 16:
			mBgColor = "#F49563";
			index = 3;
			rank = 4;
			break;
		case 32:
			mBgColor = "#F5794D";
			index = 4;
			rank = 5;
			break;
		case 64:
			mBgColor = "#F55D37";
			index = 5;
			rank = 6;
			break;
		case 128:
			mBgColor = "#EEE863";
			index = 6;
			rank = 7;
			break;
		case 256:
			mBgColor = "#EDB04D";
			index = 7;
			rank = 8;
			break;
		case 512:
			mBgColor = "#ECB04D";
			index = 8;
			rank = 9;
			break;
		case 1024:
			mBgColor = "#EB9437";
			index = 9;
			rank = 10;
			break;
		case 2048:
			mBgColor = "#EA7821";
			index = 10;
			rank = 11;
			break;
		case 4096:
			mBgColor = "#ffda47";
			index = 11;
			rank = 12;
			break;	
		case 8192:
			mBgColor = "#f86a38";
			index = 12;
			rank = 13;
			break;
		default:
			mBgColor = "#f86a38";
			index = 12;
			break;
		}

		mPaint.setColor(Color.parseColor(mBgColor));
		mPaint.setStyle(Style.FILL);
		canvas.drawRect(0, 0, getWidth(), getHeight(), mPaint);

		if (mNumber != 0)
			canvas.drawBitmap(mBitmaps[index], null, new Rect(0, 0, getWidth(),
					getHeight()), null);
			//drawText(canvas);

	}
	
	public int getrank(){
		return rank;
	}

	/**
	 * 绘制文字
	 * 
	 * @param canvas
	 */
/*	private void drawText(Canvas canvas)
	{
		
		mPaint.setColor(Color.BLACK);
		float x = (getWidth() - mBound.width()) / 2;
		float y = getHeight() / 2 + mBound.height() / 2;
		canvas.drawText(mNumberVal, x, y, mPaint);
	}*/

}

/*
 * 很简单，基本就一个onDraw通过number来绘制背景和数字；number通过
 * 调用setNumer进行设置；它的宽和高都是固定值，所以我们并不需要自己进行测量~~
 */
