import Mock from 'mockjs'

Mock.mock('/getNewslist/',{
    'list|5':[
        {
            url:'@url',
            title:'@ctitle(5,20)'
        }
    ]
})