#移動平均
class MoveAverage:
    __total = 0.0        # データの積算値
    __len = 10           # 移動平均を取るデータの個数
    __topDataIdx = -1    # 現在の最新データ格納位置
    __dataList = [0.0] * __len   # データリスト

    def __init__(self, len = 10):
        self.setLen( len )

    # 移動平均を取るデータの個数を変更
    def setLen( self, len ):
        if ( len <= 0 ):
            return False
        self.__len = len
        self.clear()

    # データを追加
    def add( self, data ):
        # 最新データを追加し最古データを除く
        self.__topDataIdx = ( self.__topDataIdx + 1 ) % self.__len
        self.__total += data - self.__dataList[ self.__topDataIdx ]
        self.__dataList[ self.__topDataIdx ] = data
        return self.average()

    # 現在の平均値を取得
    def average( self ):
        return self.__total / self.__len
    
    # データをクリア
    def clear( self ):
        self.__total = 0.0
        self.__dataList = [0.0] * self.__len
        self.__topDataIdx = -1
