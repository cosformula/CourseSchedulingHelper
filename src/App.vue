<template>
  <div id="app">
    <el-container style="height:100vh;">
      <el-header style="background: #99a9bf;">
        <el-row style="height:100%;color:white;" justify="space-between" type="flex" align="middle">
          <!-- <el-col :span="12">
            <div class="grid-content">测试 </div>
          </el-col> -->
          <el-col :span="8" style="text-align:left;color:white;">
            <el-button-group style="">
              <el-button type="primary" @click="saveData">保存</el-button>
              <el-button type="primary" @click="readData">读取</el-button>
              <el-button type="primary" @click="dialogVisible = true">导出</el-button>
              <el-button type="primary" @click="clearData">清空</el-button>
            </el-button-group>
          </el-col>
          <el-col :span="8">
            <div class="grid-content" style="text-align:center;font-size:20px;color:white;">
              上海大学排课助手
              <span style="color:#eee;font-size:0.8rem;"> 18-19年冬</span>
            </div>
          </el-col>
          <el-col :span="8" style="text-align:right;color:white;">
            <!-- <el-button-group style="">
              <el-button type="primary" @click="saveData">保存</el-button>
              <el-button type="primary" @click="readData">读取</el-button>
              <el-button type="primary" @click="dialogVisible = true">导出</el-button>
              <el-button type="primary" @click="clearData">清空</el-button>
            </el-button-group> -->
            <el-button-group style="">
              <el-tooltip effect="dark" content="在页面内打开选课系统" placement="bottom">
                <el-button type="primary" @click="dialogXkVisible = true">快捷选课</el-button>
              </el-tooltip>
              <el-button type="primary" @click="dialogAboutVisible = true">赞助</el-button>
              <el-button type="primary" @click="shuhelper">返回主站</el-button>
            </el-button-group>
            <el-button type="success">已选学分:{{ credit }}</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-main style="padding:0;box-sizing:border-box;height:100%;">
        <el-row style="padding:10px 10px 0px 10px;height:calc(100vh - 70px);">
          <el-col :xs="8" :md="8" style="height:100%;">
            <schedule :task-detail="courseSelected" @showDetail="showDetail" />
          </el-col>
          <el-col :xs="16" :md="16" style="height:100%;">
            <el-tabs type="border-card" :tab-position="'top'" style="height:calc(100% - 60px);">
              <el-tab-pane label="待选课程">
                <waitcourse :courseWaited="courseWaited" @addSchedule="addSchedule" @delCourse="delCourse" />
              </el-tab-pane>
              <el-tab-pane label="搜索课程">
                <searchcourse @addCourse="addCourse" />
              </el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
      </el-main>
      <el-dialog fullscreen title="18-19冬季学期选课系统" :visible.sync="dialogXkVisible">
        <el-row>
          <el-col :span="4">
            <ol>
              <li v-for="item in courseWaited" v-if="item.status=='已选入'">
                {{ item.course_name }}，{{item.teacher_name}}<br/>课程号：{{item.course_no}}<br/>教师号：{{item.teacher_no}}
              </li>
            </ol>
          </el-col>
          <el-col :span="20">
            <iframe src="http://xk.autoisp.shu.edu.cn:80/" width="100%" height="600"></iframe>
          </el-col>
        </el-row>
      </el-dialog>
      <el-dialog title="分享课表" v-model="dialogShareVisible" size="small">
        <p align="center" v-if="code==''">链接生成中请耐心等待...</p>
        <p align="center" v-if="code!=''">短链接已生成，您现在可以在任何地方通过
          <a :href="'http://xk.shuhelper.cn/'+code" target="_blank">http://xk.shuhelper.cn/{{ code }}</a>访问您的课表，也可以将这个链接分享给他人。</p>
      </el-dialog>
      <el-dialog width="90%" title="关于我们" :visible.sync="dialogAboutVisible" size="midumn">
        <p>排课助手(xk.shuhelper.cn)是SHUhelper的一部分，主要是为了解决排课过程中的困难而制作的小工具，主要实现了搜索课程并从心仪的课程中排列出一份完美的课表的功能。</p>
        <p> 欢迎关注我们的微信公众号 搜索：
          <span style="color:red;">shuhelper</span>
        </p>
        <p style="color:red;font-size:0.9rem;font-weight:bold;"> 也请考虑赞助以支持我们的发展(*˘︶˘*).。.:*♡
        </p>
        <p align="center">
          <img width="150" src="https://static.shuhelper.cn/formula/res/wechat.png-payment">
          <img width="150" src="https://static.shuhelper.cn/formula/res/alipay.jpg-payment">
          <!-- <img width="100" src="https://static.shuhelper.cn/mp.jpg"> -->
        </p>
        <p align="center">
          <a href="https://github.com/cosformula/CourseSchedulingHelper" target="_blank">开源代码</a>
        </p>
        <p align="center">
          <img src="http://forthebadge.com/images/badges/built-with-love.svg" />
          <img src="http://forthebadge.com/images/badges/uses-js.svg" />
          <img src="http://forthebadge.com/images/badges/makes-people-smile.svg" />
        </p>
        <blockquote style="color:grey;">遇到问题请加qq群：
          <span style="color:red;">368238744</span> 反馈</blockquote>
        <blockquote style="color:grey;">Version 0.11.0 | admin@shuhelper.cn | SHUhelper 开发委员会</blockquote>
        <blockquote>
          <span style="color:red;">♥</span>
          <span style="color:grey;">Do have faith in what you're doing.</span>
        </blockquote>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogAboutVisible = false">确 定</el-button>
        </span>
      </el-dialog>
      <el-dialog title="当前选课结果" :visible.sync="dialogVisible" size="tiny">
        <ol>
          <li v-for="item in courseWaited" v-if="item.status=='已选入'">
            {{ item.course_name }},{{item.teacher_name}},{{item.course_no}},{{item.teacher_no}}
          </li>
        </ol>
      </el-dialog>
    </el-container>
  </div>
</template>

<script>
import TopNav from './components/TopNav.vue'
import Schedule from './components/Schedule.vue'
import Waitcourse from './components/Waitcourse.vue'
import Searchcourse from './components/Searchcourse.vue'
var cn_num = {
  一: 1,
  二: 2,
  三: 3,
  四: 4,
  五: 5
}
export default {
  components: {
    Schedule,
    Waitcourse,
    Searchcourse,
    TopNav
  },
  data() {
    return {
      courseWaited: [],
      dialogXkVisible: false,
      dialogAboutVisible: false,
      dialogVisible: false,
      dialogShareVisible: false,
      code: '',
      storageKey: 'courseWaited:18-2'
    }
  },
  created: function() {
    // var code = this.getCode()
    // if (code == null) {
    //   this.readData()
    // } else {
    //   this.pull(code)
    // }
  },
  mounted() {
    this.readData()
  },
  computed: {
    credit: function() {
      var credit = 0
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].status == '已选入') {
          credit += parseInt(this.courseWaited[i].credit)
        }
      }
      return credit
    },
    timeTable: function() {
      var table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].status == '已选入') {
          var timelist = this.coursetimeToNum(this.courseWaited[i].time)
          for (var j = timelist.length - 1; j >= 0; j--) {
            var day = timelist[j].day
            for (var x = timelist[j].Start; x <= timelist[j].End; x++) {
              table[day][x] = 1
            }
          }
        }
      }
      return table
    },
    courseSelected: function() {
      // console.log('courseSelected')
      var selected = [[], [], [], [], []]
      // console.log(this.courseWaited)
      for (let i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].status == '已选入') {
          // debugger
          let timeString = this.courseWaited[i].time
          // console.log(this.courseWaited[i])
          // debugger
          var timelist = this.coursetimeToNum(timeString)
          var color = ['#2B2E4A', '#521262', '#903749', '#53354A', '#40514E', '#537780', '#3765a4', '#76a5a4', '#579870', '#e391b4', '#b8954e']
          var course = this.courseWaited[i]
          let colorIndex = Math.abs(this.hashCode(course.course_name) % color.length)
          console.log(colorIndex)
          var rancolor = color[colorIndex]

          for (var j = timelist.length - 1; j >= 0; j--) {
            var time = timelist[j]
            var item = {
              day: time.day,
              Start: time.Start,
              End: time.End,
              coursename: course.course_name,
              course_no: course.course_no,
              teachname: course.teacher_name,
              teacher_no: course.teacher_no,
              status: course.status,
              styleObj: {
                height: (time.End - time.Start + 1) * 7.7 + '%',
                top: (time.Start - 1) * 7.69 + '%',
                backgroundColor: rancolor
              }
            }
            selected[time.day].push(item)
          }
        }
      }
      return selected
    }
  },
  methods: {
    hashCode: function(s) {
      var h = 0,
        l = s.length,
        i = 0
      if (l > 0) while (i < l) h = ((h << 5) - h + s.charCodeAt(i++)) | 0
      return h
    },
    getCode: function() {
      return decodeURIComponent((new RegExp('n/' + '([^&;]+?)(&|#|;|$)').exec(location.href) || [, ''])[1].replace(/\+/g, '%20')) || null
    },
    pull: function(code) {
      this.$http
        .get('/api/pull?code=' + code)
        .then(response => {
          this.courseWaited = response.data
          this.$message({
            message: '已成功拉取云端的数据',
            type: 'success'
          })
        })
        .catch(function(response) {
          console.log(response)
        })
    },
    push: function() {
      this.dialogShareVisible = true
      this.code = ''
      this.$http
        .post('/api/push', JSON.stringify(this.courseWaited))
        .then(response => {
          this.$message({
            message: '已成功推送数据到云端',
            type: 'success'
          })
          this.code = response.data
        })
        .catch(function(response) {
          console.log(response)
        })
    },
    showDetail: function(course) {
      this.$confirm('从课表中删除' + course.coursename + course.teachname + ', 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.delCourse(course)
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        })
        .catch(err => {
          // console.log(err)
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    addCourse: function(course) {
      var conflict = false
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].course_no == course.course_no && this.courseWaited[i].teacher_no == course.teacher_no) {
          conflict = true
          break
        }
      }
      if (conflict) {
        this.$message({
          message: '已经加入过此课程',
          type: 'warning'
        })
      } else {
        this.$set(course, 'status', '待加入')
        this.courseWaited.push(course)
        this.$message({
          message: '已将此课程加入待选课程列表',
          type: 'success'
        })
      }
    },
    coursetimeToNum(time) {
      // debugger
      // console.log(time)
      var patt = /([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*/
      var timelist = []
      var str = time
      while (patt.test(str)) {
        var coursetime = patt.exec(str)
        str = str.replace(patt, '')
        var item = {
          day: parseInt(cn_num[coursetime[1]] - 1),
          Start: parseInt(coursetime[2]),
          End: parseInt(coursetime[3])
        }
        timelist.push(item)
      }
      // console.log('success to num', timelist)
      return timelist
    },
    locateCourse(course) {
      // console.log(course, 'locate')
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].course_no == course.course_no && this.courseWaited[i].teacher_no == course.teacher_no) {
          return i
        }
      }
      return -1
    },
    addSchedule: function(course) {
      //检测待加入的课程是否有冲突
      var index = this.locateCourse(course)
      var conflict = false
      var timelist = this.coursetimeToNum(this.courseWaited[index].time)
      for (var i = timelist.length - 1; i >= 0; i--) {
        for (var j = timelist[i].Start; j <= timelist[i].End; j++) {
          if (this.timeTable[timelist[i].day][j] != 0) {
            conflict = true
          }
        }
      }
      if (conflict) {
        this.$message({
          message: '课程时间冲突！',
          type: 'warning'
        })
      } else {
        this.$set(this.courseWaited[index], 'status', '已选入')
        this.$message({
          message: '已将此课程加入课程表',
          type: 'success'
        })
        // this.$http.get(`/api/courses/${this.courseWaited[index]._id.$oid}`)
      }
    },
    delCourse: function(course) {
      var index = this.locateCourse(course)
      if (course.status == '已选入') {
        this.$set(this.courseWaited[index], 'status', '待加入')
      } else {
        this.courseWaited.splice(index, 1)
      }
      this.$message({
        message: '已成功删除该课程',
        type: 'success'
      })
    },
    saveData() {
      var courseWaited = JSON.stringify(this.courseWaited)
      localStorage.setItem(this.storageKey, courseWaited)
      this.$message({
        message: '已成功保存当前状态',
        type: 'success'
      })
    },
    refreshData() {
      for (let i = 0; i < this.courseWaited.length; i++) {
        let course = this.courseWaited[i]
        this.$http.get(`/api/courses/class/${course._id.$oid}`).then(response => {
          let status = course.status
          let newCourse = response.data.course
          this.courseWaited[i].capacity = newCourse.capacity
          this.courseWaited[i].enroll = newCourse.enroll
          this.courseWaited[i].teacher_name = newCourse.teacher_name
        })
      }
    },
    readData() {
      let courses
      try {
        courses = JSON.parse(localStorage.getItem(this.storageKey))
      } catch (error) {
        courses = []
      }
      if (courses.length) {
        this.courseWaited = []
        this.courseWaited.push(...courses)
        this.$message({
          message: '已成功读取上次的数据',
          type: 'success'
        })
        this.refreshData()
      } else {
        this.$message({
          message: '无数据',
          type: 'warning'
        })
      }
    },
    clearData() {
      this.$confirm('此操作将删除目前的选课结果且无法恢复, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.courseWaited = []
          timetableinit()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    shuhelper() {
      window.open('https://www.shuhelper.cn/')
    }
  }
}
</script>

<style>
html body {
  font-family: Helvetica, sans-serif;
  margin: 0;
}
</style>
