1.在此資料夾下，terminal執行 "python sphere.py" 指令，獲得球體模型的obj、mtl檔案，且會額外輸出一張"前鏡頭左右反轉"影像
2.結合完成後會顯示完成說明，按下"ESC"離開，並保存obj、mtl檔案
3.terminal執行 "python m10802152.py" 指令，開始觀看side-by-side 360-degree圖
4.滑鼠左建:球體旋轉、滑鼠滾輪:球體放大縮小
  鍵盤"F":還原初始位置、鍵盤"ESC":離開

P.S.程式裡有註解


用角度計算出每個Vertex、Vertex Normal，再來將Vertex * 0.802得到Texture Coordinate，" * 0.802 "是因為要將U-V texture coordinates大概調整到180度位置上。
另外還需要將前景圖進行左右翻轉，以利U-V texture coordinates方便計算。