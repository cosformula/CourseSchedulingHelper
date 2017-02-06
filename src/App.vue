<template>
  <div id="app">
  <el-row>
    <el-col :span="8"><schedule 
          :task-detail="courseSelected"
          /></el-col>
    <el-col :span="16">
    <el-row>
    <el-col :span="24">
    <img src="http://forthebadge.com/images/badges/built-with-love.svg"/>
    <img src="http://forthebadge.com/images/badges/uses-js.svg"/>
    <img src="http://forthebadge.com/images/badges/makes-people-smile.svg"/>
     </el-col>
    </el-row>
    <el-row>
     <el-col :span="24">
     <div style="padding-top:0.5rem;padding-bottom:0.5rem;">
     <el-button-group>
      <el-button type="primary"  @click="saveData">保存</el-button>
      <el-button type="primary"  @click="readData">读取</el-button>
      <el-button type="primary"  @click="dialogVisible = true">导出</el-button>
      <el-button type="primary"  @click="clearData">清空</el-button>
      </el-button-group>
      <el-button-group>
      <el-button type="primary"  @click="about">关于我们</el-button>
      <el-button type="primary"  @click="blog">开发博客</el-button>
      <el-button type="primary"  @click="github">开源代码</el-button>
      </el-button-group>
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
function timetableinit(){
  timetable = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  ]
}
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
    saveData(){
      var courseWaited = JSON.stringify(this.courseWaited)
      localStorage.setItem('courseWaited',courseWaited);
      var courseSelected = JSON.stringify(this.courseSelected)
      localStorage.setItem('courseSelected',courseSelected);
      var timetableString = JSON.stringify(timetable)
      localStorage.setItem('timetable',timetableString); 
      this.$message({
          message: '已成功保存当前状态',
          type: 'success'
        });
    },
    readData(){
      if(JSON.parse(localStorage.getItem('courseWaited'))&&JSON.parse(localStorage.getItem('courseSelected'))){
        this.courseWaited = JSON.parse(localStorage.getItem('courseWaited'))
        this.courseSelected = JSON.parse(localStorage.getItem('courseSelected'))
        timetable = JSON.parse(localStorage.getItem('timetable'))
        this.$message({
            message: '已成功读取上次的数据',
            type: 'success'
          });
      }
      else{
        this.$message({
            message: '无数据',
            type: 'warning'
          });
      }
      
    },
    clearData(){
      this.$confirm('此操作将删除目前的选课结果且无法恢复, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.courseWaited = []
          this.courseSelected = [[],[],[],[],[]]
          timetableinit()
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
    },
    blog(){
      window.open('http://blog.shuhelper.cn/')
    },
    github(){
      window.open('https://github.com/cosformula/CourseSchedulingHelper')
    },
    about() {
        this.$alert('当前版本0.3.2_cosformula@t.shu.edu.cn_SHUhelper开发委员会', '选课助手', {
          confirmButtonText: '确定',
        })
    }
  }
}
</script>

<style>
body {
  font-family: Helvetica, sans-serif;
}
</style>
