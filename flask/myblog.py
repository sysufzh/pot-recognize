from app import app

#防止被引用后执行，只有在当前模块中才可以使用
if __name__=='__main__':
    app.run(debug=False,port=5629,host='0.0.0.0')
