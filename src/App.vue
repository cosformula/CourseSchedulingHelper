<template lang="html">
  <div id="app">
    <el-container>
      <el-header  style="text-align: right; ">
        <span style="color:black;float:left;">上海大学排课助手   <span style="color:grey;font-size:0.8rem;">  17-18年春</span>   </span>
        <el-button-group style="">
          <el-button type="primary"
                    @click="saveData">保存</el-button>
          <el-button type="primary"
                    @click="readData">读取</el-button>
          <el-button type="primary"
                    @click="dialogVisible = true">导出</el-button>
          <el-button type="primary"
                    @click="clearData">清空</el-button>
        </el-button-group>
        <el-button-group style="">
          <el-tooltip effect="dark"
                      content="在页面内打开选课系统"
                      placement="bottom">
            <el-button type="primary"
                      @click="dialogXkVisible = true">快捷选课</el-button>
          </el-tooltip>
          <el-button type="primary"
                      @click="dialogAboutVisible = true">关于</el-button>
          <el-button type="primary"
                      @click="shuhelper">返回SHUhelper</el-button>
        </el-button-group>
        <el-button type="success" >已选学分:{{ credit }}</el-button>
      </el-header>
      <el-main>
        <el-row style="padding:0;">
          <el-col :xs="8" :md="8"
                  style="min-height:700px;height:90vh;max-height:1000px;">
            <schedule :task-detail="courseSelected"
                      @showDetail="showDetail" />
          </el-col>
          <el-col :xs="16" :md="16">
            <el-tabs type="border-card" :tab-position="'top'">
              <el-tab-pane label="待选课程">
                <waitcourse :courseWaited="courseWaited"
                            @addSchedule="addSchedule"
                            @delCourse="delCourse"/>
              </el-tab-pane>
              <el-tab-pane label="搜索课程">
                <searchcourse @addCourse="addCourse"/>
              </el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
      </el-main>
      <el-dialog title="17-18春季学期选课系统"
                    :visible.sync="dialogXkVisible"
                    width="80%">
      <el-row>
        <el-col :span="6">
          <ol>
            <li v-for="item in courseWaited"
                v-if="item.status=='已选入'">
              {{ item.course_name }},{{item.teacher_name}},{{item.course_no}},{{item.teacher_no}}
            </li>
          </ol>
        </el-col>
        <el-col :span="18">
          <iframe src="http://xk.autoisp.shu.edu.cn:8080/"
                  width="100%"
                  height="500"></iframe>
        </el-col>
      </el-row>
    </el-dialog>
    <el-dialog title="分享课表"
                v-model="dialogShareVisible"
                size="small">
      <p align="center"
          v-if="code==''">链接生成中请耐心等待...</p>
      <p align="center"
          v-if="code!=''">短链接已生成，您现在可以在任何地方通过
        <a :href="'http://xk.shuhelper.cn/'+code"
            target="_blank">http://xk.shuhelper.cn/{{ code }}</a>访问您的课表，也可以将这个链接分享给他人。</p>
    </el-dialog>
    <el-dialog title="关于我们"
                :visible.sync="dialogAboutVisible"
                size="small">
      <p>排课助手(xk.shuhelper.cn)是SHUhelper的一部分，主要是为了解决排课过程中的困难而制作的小工具，主要实现了搜索课程并从心仪的课程中排列出一份完美的课表的功能。</p>
      <p> 欢迎关注我们的微信公众号 搜索：
        <span style="color:red;">shuhelper</span> 或扫描下方二维码</p>
      <p align="center">
        <img width="100"
              src="https://static.shuhelper.cn/mp.jpg">
      </p>
      <p align="center">
        <a href="https://github.com/cosformula/CourseSchedulingHelper"
            target="_blank">开源代码</a>
      </p>
      <p align="center">
        <img src="http://forthebadge.com/images/badges/built-with-love.svg" />
        <img src="http://forthebadge.com/images/badges/uses-js.svg" />
        <img src="http://forthebadge.com/images/badges/makes-people-smile.svg" />
      </p>
      <blockquote style="color:grey;">遇到问题请加qq群：
        <span style="color:red;">368238744</span> 反馈</blockquote>
      <blockquote style="color:grey;">Version 0.10.0 | admin@shuhelper.cn | SHUhelper 开发委员会</blockquote>
      <blockquote>
        <span style="color:red;">♥</span>
        <span style="color:grey;">Do have faith in what you're doing.</span>
      </blockquote>
      <span slot="footer"
            class="dialog-footer">
        <el-button type="primary"
                    @click="dialogAboutVisible = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="当前选课结果"
                :visible.sync="dialogVisible"
                size="tiny">
      <ol>
        <li v-for="item in courseWaited"
            v-if="item.status=='已选入'">
          {{ item.course_name }},{{item.teacher_name}},{{item.course_no}},{{item.teacher_no}}
        </li>
      </ol>
    </el-dialog>
    </el-container>
  </div>
</template>

<script>
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
    Searchcourse
  },
  data() {
    return {
      courseWaited: [],
      dialogXkVisible: false,
      dialogAboutVisible: false,
      dialogVisible: false,
      dialogShareVisible: false,
      code: ''
    }
  },
  created: function() {
    var code = this.getCode()
    if (code == null) {
      this.readData()
    } else {
      this.pull(code)
    }
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
      console.log('courseSelected')
      var selected = [[], [], [], [], []]
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].status == '已选入') {
          var timelist = this.coursetimeToNum(this.courseWaited[i].time)
          var color = ['#2B2E4A', '#521262', '#903749', '#53354A', '#40514E', '#537780']
          var course = this.courseWaited[i]
          var rancolor = color[~~(Math.random() * color.length)]
          for (var j = timelist.length - 1; j >= 0; j--) {
            var time = timelist[j]
            var item = {
              day: time.day,
              Start: time.Start,
              End: time.End,
              coursename: course.course_name,
              courseno: course.course_no,
              teachname: course.teacher_name,
              teachno: course.teacher_no,
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
        .catch(() => {
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
<<<<<<< HEAD
        })
      } else {
=======
        });
      }
      else {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
        this.$set(course, 'status', '待加入')
        this.courseWaited.push(course)
        this.$message({
          message: '已将此课程加入待选课程列表',
          type: 'success'
        })
      }
    },
<<<<<<< HEAD
    coursetimeToNum(time) {
=======
    coursetimeToNum (time) {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
      var patt = /([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*/
      var timelist = []
      var str = time
      while (patt.test(str)) {
        var coursetime = patt.exec(str)
<<<<<<< HEAD
        str = str.replace(patt, '')
=======
        str = str.replace(patt, "")
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
        var item = {
          day: parseInt(cn_num[coursetime[1]] - 1),
          Start: parseInt(coursetime[2]),
          End: parseInt(coursetime[3])
        }
        timelist.push(item)
      }
      return timelist
    },
<<<<<<< HEAD
    locateCourse(course) {
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].course_no == course.course_no && this.courseWaited[i].teacher_no == course.teacher_no) {
=======
    locateCourse (course) {
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].courseno == course.courseno && this.courseWaited[i].teachno == course.teachno) {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
          return i
        }
      }
      return -1
    },
<<<<<<< HEAD
    addSchedule: function(course) {
      //检测待加入的课程是否有冲突
      var index = this.locateCourse(course)
      var conflict = false
      var timelist = this.coursetimeToNum(this.courseWaited[index].time)
=======
    addSchedule: function (course) {
      //检测待加入的课程是否有冲突
      var index = this.locateCourse(course)
      var conflict = false
      var timelist = this.coursetimeToNum(this.courseWaited[index].coursetime)
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
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
<<<<<<< HEAD
        })
      } else {
=======
        });
      }
      else {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
        this.$set(this.courseWaited[index], 'status', '已选入')
        this.$message({
          message: '已将此课程加入课程表',
          type: 'success'
        })
      }
    },
<<<<<<< HEAD
    delCourse: function(course) {
=======
    delCourse: function (course) {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
      var index = this.locateCourse(course)
      console.log('delcourse')
      if (course.status == '已选入') {
        this.$set(this.courseWaited[index], 'status', '待加入')
<<<<<<< HEAD
      } else {
=======
      }
      else {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
        this.courseWaited.splice(index, 1)
      }
      this.$message({
        message: '已成功删除该课程',
        type: 'success'
<<<<<<< HEAD
      })
    },
    saveData() {
      var courseWaited = JSON.stringify(this.courseWaited)
      localStorage.setItem('courseWaited', courseWaited)
      this.$message({
        message: '已成功保存当前状态',
        type: 'success'
      })
    },
    readData() {
=======
      });
    },
    saveData () {
      var courseWaited = JSON.stringify(this.courseWaited)
      localStorage.setItem('courseWaited', courseWaited);
      this.$message({
        message: '已成功保存当前状态',
        type: 'success'
      });
    },
    readData () {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
      if (JSON.parse(localStorage.getItem('courseWaited'))) {
        this.courseWaited = JSON.parse(localStorage.getItem('courseWaited'))
        this.$message({
          message: '已成功读取上次的数据',
          type: 'success'
<<<<<<< HEAD
        })
      } else {
        this.$message({
          message: '无数据',
          type: 'warning'
        })
      }
    },
    clearData() {
=======
        });
      }
      else {
        this.$message({
          message: '无数据',
          type: 'warning'
        });
      }
    },
    clearData () {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
      this.$confirm('此操作将删除目前的选课结果且无法恢复, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
<<<<<<< HEAD
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
=======
      }).then(() => {
        this.courseWaited = []
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
    shuhelper () {
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
      window.open('https://www.shuhelper.cn/')
    }
  }
}
</script>

<style>
html body {
  font-family: Helvetica, sans-serif;
<<<<<<< HEAD
  margin:0;
}
=======
}

html,
body {
  height: 100%;
  margin: 0;
}

#app {
  height: 100%;
}
>>>>>>> b9003694b20dbd0980a959a73ae0a7349f04515d
</style>
