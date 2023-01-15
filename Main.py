from server.app import main, app

if __name__ == '__main__':
    main()
    app.run(host='192.168.137.220', port=5000, debug=True)