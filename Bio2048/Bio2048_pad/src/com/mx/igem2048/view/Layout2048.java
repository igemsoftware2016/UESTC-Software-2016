package com.mx.igem2048.view;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.util.TypedValue;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.widget.RelativeLayout;

/**
 * 2048鐨勬父鎴忛潰鏉匡紝鍔犲叆甯冨眬鏂囦欢鍗冲彲寮�濮嬫父鎴�
 * 
 * @author zhy
 * 
 */
public class Layout2048 extends RelativeLayout
{

	/**
	 * 璁剧疆Item鐨勬暟閲弉*n锛涢粯璁や负4
	 */
	private int mColumn = 4;
	/**
	 * 瀛樻斁鎵�鏈夌殑Item
	 */
	private Item2048[] mGame2048Items;

	/**
	 * Item妯悜涓庣旱鍚戠殑杈硅窛锛屽杈硅窛
	 */
	private int mMargin = 10;
	/**
	 * 闈㈡澘鐨刾adding锛屽唴杈硅窛
	 */
	private int mPadding;
	/**
	 * 妫�娴嬬敤鎴锋粦鍔ㄧ殑鎵嬪娍
	 */
	private GestureDetector mGestureDetector;

	// 鐢ㄤ簬纭鏄惁闇�瑕佺敓鎴愪竴涓柊鐨勫��
	private boolean isMergeHappen = true;
	private boolean isMoveHappen = true;

	/**
	 * 璁板綍鍒嗘暟
	 */
	private int mScore;
	
	public int getHighestRank(){
		int i=0,j=0;//j用来记录最大rank的位置
		for( ; i < mColumn*mColumn; i++)
			if(mGame2048Items[j].getrank()<mGame2048Items[i].getrank())
				j=i;					
		return mGame2048Items[j].getrank();
	}
	
	public  void setmColumn(int num){mColumn =num;}

	public interface OnGame2048Listener
	{
		void onScoreChange(int score);

		void onGameOver();

		void onRankChange();
		
	}

	private OnGame2048Listener mGame2048Listener;

	public void setOnGame2048Listener(OnGame2048Listener mGame2048Listener)
	{
		this.mGame2048Listener = mGame2048Listener;
	}

	/**
	 * 杩愬姩鏂瑰悜鐨勬灇涓�
	 * 
	 * @author zhy
	 * 
	 */
	private enum ACTION
	{
		LEFT, RIGHT, UP, DOWM
	}

	public Layout2048(Context context, AttributeSet attrs, int defStyle)
	{
		super(context, attrs, defStyle);

		mMargin = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP,
				mMargin, getResources().getDisplayMetrics());
		// 璁剧疆Layout鐨勫唴杈硅窛锛屽洓杈逛竴鑷达紝璁剧疆涓哄洓鍐呰竟璺濅腑鐨勬渶灏忓��
		mPadding = min(getPaddingLeft(), getPaddingTop(), getPaddingRight(),
				getPaddingBottom());

		mGestureDetector = new GestureDetector(context , new MyGestureDetector());

	}

	/**
	 * 鏍规嵁鐢ㄦ埛杩愬姩锛屾暣浣撹繘琛岀Щ鍔ㄥ悎骞跺�肩瓑
	 */
	private void action(ACTION action)
	{
		mGame2048Listener.onRankChange();
		// 琛寍鍒�
		for (int i = 0; i < mColumn; i++)
		{
			List<Item2048> row = new ArrayList<Item2048>();
			// 琛寍鍒�
			//璁板綍涓嶄负0鐨勬暟瀛�
			for (int j = 0; j < mColumn; j++)
			{
				// 寰楀埌涓嬫爣
				int index = getIndexByAction(action, i, j);

				Item2048 item = mGame2048Items[index];
				// 璁板綍涓嶄负0鐨勬暟瀛�
				if (item.getNumber() != 0)
				{
					row.add(item);
				}
			}
			
			//鍒ゆ柇鏄惁鍙戠敓绉诲姩
			for (int j = 0; j < mColumn && j < row.size(); j++)
			{
				int index = getIndexByAction(action, i, j);
				Item2048 item = mGame2048Items[index];

				if (item.getNumber() != row.get(j).getNumber())
				{
					isMoveHappen = true;
				}
			}
			
			// 鍚堝苟鐩稿悓鐨�
			mergeItem(row);
			
			// 璁剧疆鍚堝苟鍚庣殑鍊�
			for (int j = 0; j < mColumn; j++)
			{
				int index = getIndexByAction(action, i, j);
				if (row.size() > j)
				{
					mGame2048Items[index].setNumber(row.get(j).getNumber());
				} else
				{
					mGame2048Items[index].setNumber(0);
				}
			}

		}
		//鐢熸垚鏁板瓧
		generateNum();

	}

	/**
	 * 鏍规嵁Action鍜宨,j寰楀埌涓嬫爣
	 * 
	 * @param action
	 * @param i
	 * @param j
	 * @return
	 */
	private int getIndexByAction(ACTION action, int i, int j)
	{
		int index = -1;
		switch (action)
		{
		case LEFT:
			index = i * mColumn + j;
			break;
		case RIGHT:
			index = i * mColumn + mColumn - j - 1;
			break;
		case UP:
			index = i + j * mColumn;
			break;
		case DOWM:
			index = i + (mColumn - 1 - j) * mColumn;
			break;
		}
		return index;
	}

	/**
	 * 鍚堝苟鐩稿悓鐨処tem
	 * 
	 * @param row
	 */
	private void mergeItem(List<Item2048> row)
	{
		if (row.size() < 2)
			return;

		for (int j = 0; j < row.size() - 1; j++)
		{
			Item2048 item1 = row.get(j);
			Item2048 item2 = row.get(j + 1);

			if (item1.getNumber() == item2.getNumber())
			{
				isMergeHappen = true;

				int val = item1.getNumber() + item2.getNumber();
				item1.setNumber(val);

				// 鍔犲垎
				mScore += val;
				if (mGame2048Listener != null)
				{
					mGame2048Listener.onScoreChange(mScore);
				}

				// 鍚戝墠绉诲姩
				for (int k = j + 1; k < row.size() - 1; k++)
				{
					row.get(k).setNumber(row.get(k + 1).getNumber());
				}
				
				row.get(row.size() - 1).setNumber(0);
				return;
			}

		}

	}

	/**
	 * 寰楀埌澶氬�间腑鐨勬渶灏忓��
	 * 
	 * @param params
	 * @return
	 */
	private int min(int... params)
	{
		int min = params[0];
		for (int param : params)
		{
			if (min > param)
			{
				min = param;
			}
		}
		return min;
	}

	@Override
	public boolean onTouchEvent(MotionEvent event)
	{
		mGestureDetector.onTouchEvent(event);
		return true;
	}

	public Layout2048(Context context)
	{
		this(context, null);
	}

	public Layout2048(Context context, AttributeSet attrs)
	{
		this(context, attrs, 0);
	}

	private boolean once;

	/**
	 * 娴嬮噺Layout鐨勫鍜岄珮锛屼互鍙婅缃甀tem鐨勫鍜岄珮锛岃繖閲屽拷鐣rap_content 浠ュ銆侀珮涔嬩腑鐨勬渶灏忓�肩粯鍒舵鏂瑰舰
	 */
	@Override
	protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec)
	{
		super.onMeasure(widthMeasureSpec, heightMeasureSpec);
		// 鑾峰緱姝ｆ柟褰㈢殑杈归暱
		int length = Math.min(getMeasuredHeight(), getMeasuredWidth());
		// 鑾峰緱Item鐨勫搴�
		int childWidth = (length - mPadding * 2 - mMargin * (mColumn - 1))
				/ mColumn;

		if (!once)
		{
			if (mGame2048Items == null)
			{
				mGame2048Items = new Item2048[mColumn * mColumn];
			}
			// 鏀剧疆Item
			for (int i = 0; i < mGame2048Items.length; i++)
			{
				Item2048 item = new Item2048(getContext());

				mGame2048Items[i] = item;
				item.setId(i + 1);
				RelativeLayout.LayoutParams lp = new LayoutParams(childWidth,
						childWidth);
				// 璁剧疆妯悜杈硅窛,涓嶆槸鏈�鍚庝竴鍒�
				if ((i + 1) % mColumn != 0)
				{
					lp.rightMargin = mMargin;
				}
				// 濡傛灉涓嶆槸绗竴鍒�
				if (i % mColumn != 0)
				{
					lp.addRule(RelativeLayout.RIGHT_OF,//
							mGame2048Items[i - 1].getId());
				}
				// 濡傛灉涓嶆槸绗竴琛岋紝//璁剧疆绾靛悜杈硅窛锛岄潪鏈�鍚庝竴琛�
				if ((i + 1) > mColumn)
				{
					lp.topMargin = mMargin;
					lp.addRule(RelativeLayout.BELOW,//
							mGame2048Items[i - mColumn].getId());
				}
				addView(item, lp);
			}
			generateNum();
		}
		once = true;

		setMeasuredDimension(length, length);
	}

	/**
	 * 鏄惁濉弧鏁板瓧
	 * 
	 * @return
	 */
	private boolean isFull()
	{
		// 妫�娴嬫槸鍚︽墍鏈変綅缃兘鏈夋暟瀛�
		for (int i = 0; i < mGame2048Items.length; i++)
		{
			if (mGame2048Items[i].getNumber() == 0)
			{
				return false;
			}
		}
		return true;
	}

	/**
	 * 浜х敓涓�涓暟瀛�
	 */
	public void generateNum()
	{
		
		if (checkOver())
		{
			Log.e("TAG", "GAME OVER");
			if (mGame2048Listener != null)
			{
				mGame2048Listener.onGameOver();
			}
			return;
		}

		if (!isFull())
		{
			if (isMoveHappen || isMergeHappen)
			{
				Random random = new Random();
				int next = random.nextInt(16);
				Item2048 item = mGame2048Items[next];

				while (item.getNumber() != 0)
				{
					next = random.nextInt(16);
					item = mGame2048Items[next];
				}

				item.setNumber(2);

				isMergeHappen = isMoveHappen = false;
			}

		}
	}

	/**
	 * 妫�娴嬪綋鍓嶆墍鏈夌殑浣嶇疆閮芥湁鏁板瓧锛屼笖鐩搁偦鐨勬病鏈夌浉鍚岀殑鏁板瓧
	 * 
	 * @return
	 */
	private boolean checkOver()
	{
		// 妫�娴嬫槸鍚︽墍鏈変綅缃兘鏈夋暟瀛�
		if (!isFull())
		{
			return false;
		}
	
		for (int i = 0; i < mColumn; i++)
		{
			for (int j = 0; j < mColumn; j++)
			{
	
				int index = i * mColumn + j;
	
				// 褰撳墠鐨処tem
				Item2048 item = mGame2048Items[index];
				// 鍙宠竟
				if ((index + 1) % mColumn != 0)
				{
					Log.e("TAG", "RIGHT");
					// 鍙宠竟鐨処tem
					Item2048 itemRight = mGame2048Items[index + 1];
					if (item.getNumber() == itemRight.getNumber())
						return false;
				}
				// 涓嬭竟
				if ((index + mColumn) < mColumn * mColumn)
				{
					Log.e("TAG", "DOWN");
					Item2048 itemBottom = mGame2048Items[index + mColumn];
					if (item.getNumber() == itemBottom.getNumber())
						return false;
				}
				// 宸﹁竟
				if (index % mColumn != 0)
				{
					Log.e("TAG", "LEFT");
					Item2048 itemLeft = mGame2048Items[index - 1];
					if (itemLeft.getNumber() == item.getNumber())
						return false;
				}
				// 涓婅竟
				if (index + 1 > mColumn)
				{
					Log.e("TAG", "UP");
					Item2048 itemTop = mGame2048Items[index - mColumn];
					if (item.getNumber() == itemTop.getNumber())
						return false;
				}
	
			}
	
		}
	
		return true;
	
	}

	/**
	 * 閲嶆柊寮�濮嬫父鎴�
	 */
	public void restart()
	{
		for (Item2048 item : mGame2048Items)
		{
			item.setNumber(0);
		}
		mScore = 0;
		if (mGame2048Listener != null)
		{
			mGame2048Listener.onScoreChange(mScore);
		}
		isMoveHappen = isMergeHappen = true;
		generateNum();
	}

	class MyGestureDetector extends GestureDetector.SimpleOnGestureListener
	{

		final int FLING_MIN_DISTANCE = 50;

		@Override
		public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX,
				float velocityY)
		{
			float x = e2.getX() - e1.getX();
			float y = e2.getY() - e1.getY();

			if (x > FLING_MIN_DISTANCE
					&& Math.abs(velocityX) > Math.abs(velocityY))
			{
				action(ACTION.RIGHT);
				// Toast.makeText(getContext(), "toRight",
				// Toast.LENGTH_SHORT).show();

			} else if (x < -FLING_MIN_DISTANCE
					&& Math.abs(velocityX) > Math.abs(velocityY))
			{
				action(ACTION.LEFT);
				// Toast.makeText(getContext(), "toLeft",
				// Toast.LENGTH_SHORT).show();

			} else if (y > FLING_MIN_DISTANCE
					&& Math.abs(velocityX) < Math.abs(velocityY))
			{
				action(ACTION.DOWM);
				// Toast.makeText(getContext(), "toDown",
				// Toast.LENGTH_SHORT).show();

			} else if (y < -FLING_MIN_DISTANCE
					&& Math.abs(velocityX) < Math.abs(velocityY))
			{
				action(ACTION.UP);
				// Toast.makeText(getContext(), "toUp",
				// Toast.LENGTH_SHORT).show();
			}
			return true;

		}

	}

}
