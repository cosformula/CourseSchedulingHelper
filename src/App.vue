<template>
  <div id="app">
  <el-row>
    <el-col :span="10"><schedule 
          :task-detail="courseSelected"
          /></el-col>
    <el-col :span="14">
    <el-row>
    <el-col :span="24">
    <img src="http://forthebadge.com/images/badges/built-with-love.svg"/>
    <img src="http://forthebadge.com/images/badges/uses-js.svg"/>
    <img src="http://forthebadge.com/images/badges/makes-people-smile.svg"/>
     </el-col>
    </el-row>
    <el-row>
     <el-col :span="24">
     <div style="padding:0.5rem;">
      <el-button type="primary"  @click="dialogVisible = true">导出当前课表</el-button>
      <el-button type="primary"  @click="open2">使用帮助</el-button>
      <el-button type="primary"  @click="open3">关于选课助手</el-button>
      <el-button type="primary"  @click="blog">开发博客</el-button>
      <el-button type="primary"  @click="open4">分享</el-button>
      </div>
      </el-col>
    </el-row>

    <el-tabs type="border-card">
      <el-tab-pane label="待选课程">
        <waitcourse :courseWaited="courseWaited" @addSchedule="addSchedule" @delCourse="delCourse"/>
      </el-tab-pane>
      <el-tab-pane label="搜索课程">
        <searchcourse @addCourse="addCourse"/>
    </el-tabs>
    </el-col>
  </el-row>
  <el-dialog title="当前选课结果" v-model="dialogVisible" size="tiny">
  <ol>
  <li v-for="item in courseWaited" v-if="item.status=='已选入'">
  {{ item.coursename }},{{item.teachname}},{{item.courseno}},{{item.teachno}}
  </li>
  </ol>
  </el-dialog>
  </div>
</template>

<script>
import Schedule from './components/Schedule.vue'
import Waitcourse from './components/Waitcourse.vue'
import Searchcourse from './components/Searchcourse.vue'
var cn_num = {
  '一':1,
  '二':2,
  '三':3,
  '四':4,
  '五':5,
}
var timetable = [
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]
export default {
  components: {
      Schedule,
      Waitcourse,
      Searchcourse
  },
  data () {
    return {
      courseWaited:[],
      courseSelected:[[],[],[],[],[]],
      dialogVisible: false
    }
  },
  computed:{

  },
  methods: {
    addCourse:function(course){
      var conflict = false
      for(var i = this.courseWaited.length-1;i>=0;i--){
        if(this.courseWaited[i].courseno==course.courseno&&this.courseWaited[i].teachno==course.teachno){
          conflict = true;
          break;
        }
      }
      if(conflict){
        this.$message({
          message: '已经加入过此课程',
          type: 'warning'
        });
      }
      else{
        this.$set(course,'status','待加入')
        this.courseWaited.push(course)
        this.$message({
          message: '已将此课程加入待选课程列表',
          type: 'success'
        });
      }
    },
    addSchedule:function(index,course){
      this.$set(this.courseWaited[index],'status','已选入')
      var title = course.coursename
      var teacher = course.teachname
      var str = course.coursetime
      var patt = /([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*/
      var items = []
      var color= [
        "#2B2E4A",
        "#521262",
        "#903749",
        "#53354A",
        "#40514E",
        "#537780",
			]
      var rancolor = color[~~(Math.random() * color.length)]
      // 创建待加入的课程
      while(patt.test(str)){
        var coursetime = patt.exec(str)
        str = str.replace(patt,"")
        var item = {
          day:parseInt(cn_num[coursetime[1]]-1),
          Start:parseInt(coursetime[2]),
          End:parseInt(coursetime[3]),
          title: title,
          teacher:teacher,
          teachno:course.teachno,
          styleObj:{
            height: (parseInt(coursetime[3])-parseInt(coursetime[2])+1) * 50+ 'px',
            top: ((parseInt(coursetime[2])-1) * 50) + 50 + 'px',
            backgroundColor: rancolor
          }  
        }
        items.push(item)
      }
      //检测待加入的课程是否有冲突
      var conflict = false
      for(var i = items.length-1;i>=0;i--){
        for(var j = items[i].Start;j <= items[i].End;j++){
          if(timetable[items[i].day][j]!=0){
            conflict = true
          }
        }
      }
      if(conflict){
        this.$message({
          message: '课程时间冲突！',
          type: 'warning'
        });
        this.$set(this.courseWaited[index],'status','待加入')
      }
      else{
        for(var i = items.length-1;i>=0;i--){
          this.courseSelected[items[i].day].push(items[i])
          for(var j = items[i].Start;j <= items[i].End;j++){
              timetable[items[i].day][j]=1
            }
          }
          this.$message({
          message: '已将此课程加入课程表',
          type: 'success'
        });
      }
    },
    delCourse:function(index,course){
      if(course.status=='已选入'){
        for(var i = 4;i>=0;i--){
          for(var j=this.courseSelected[i].length-1;j>=0;j--){
            if(this.courseSelected[i][j].title==course.coursename&&this.courseSelected[i][j].teachno==course.teachno){
              for(var x = this.courseSelected[i][j].Start;x <= this.courseSelected[i][j].End;x++){
                timetable[this.courseSelected[i][j].day][x]=0
              }
              this.courseSelected[i].splice(j,1)
            }
          }
        }
        this.$set(this.courseWaited[index],'status','待加入')
      }
      else{
        this.courseWaited.splice(index,1)
      }
      
      this.$message({
          message: '已成功删除该课程',
          type: 'success'
        });
    },
    blog(){
      window.open('http://blog.shuhelper.cn/')
    },
    open1() {
      var str = ''
      for(var i=this.courseWaited.length-1;i>=0;i--)
      {
        if(this.courseWaited[i].status=='已选入'){
          str = str + + this.courseWaited[i].courseno + this.courseWaited[i].teachno
        }
      }
        this.$alert('这是一段内容', '当前选中的课表', {
          confirmButtonText: '确定',
          callback: action => {
            this.$message({
              type: 'info',
              message: `action: ${ action }`
            });
          }
        });
    },
    open2() {
        this.$alert('等会写', '帮助', {
          confirmButtonText: '确定',
        })
    },
    open3() {
        this.$alert('当前版本0.1.3_cosformula_SHUhelper开发委员会', '选课助手', {
          confirmButtonText: '确定',
        })
    },
    open4() {
        this.$alert('xk.shuhelper.cn', '分享', {
          confirmButtonText: '确定',
        })
    },
  }
}
</script>

<style>
body {
  font-family: Helvetica, sans-serif;
}
</style>
