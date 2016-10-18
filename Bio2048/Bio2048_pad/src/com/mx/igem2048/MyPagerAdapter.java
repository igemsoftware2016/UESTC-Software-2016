package com.mx.igem2048;

import java.util.List;

import android.support.v4.view.PagerAdapter;
import android.view.View;
import android.view.ViewGroup;

public class MyPagerAdapter extends PagerAdapter{

	private List<View>viewList;
	
	public MyPagerAdapter(List<View>viewList){
		this.viewList = viewList;
	}
	
	//返回页卡数量
	@Override
	public int getCount() {
		// TODO Auto-generated method stub
		return viewList.size();
	}

	//判断View是否来自对象
	@Override
	public boolean isViewFromObject(View arg0, Object arg1) {
		// TODO Auto-generated method stub
		return arg0 == arg1;
	}
	
	//实例化一个页卡
	@Override
	public Object instantiateItem(ViewGroup container, int position){
		container.addView(viewList.get(position));
		return viewList.get(position);
	}
	
	//销毁一个页卡
	@Override
	public void destroyItem(ViewGroup container, int position, Object object){
		container.removeView(viewList.get(position));
	}

}
