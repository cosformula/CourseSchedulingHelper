<template>
  <div id="app">
    <el-row style="height:95%;padding-top:10px;">
      <el-col :span="8" style="height:100%;">
        <schedule :task-detail="courseSelected" @showDetail="showDetail" />
      </el-col>
      <el-col :span="16">
        <el-row>
          <el-col :span="24">
            <div style="padding:10px;">
              <span style="color:grey;">当前学期:16-17年春季学期</span>
            </div>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24" style="height:100%;">
            <div style="padding-top:0.5rem;padding-bottom:0.5rem;">
              <el-button-group>
                <el-button type="primary" @click="saveData">保存</el-button>
                <el-button type="primary" @click="readData">读取</el-button>
                <el-button type="primary" @click="dialogVisible = true">导出</el-button>
                <el-button type="primary" @click="clearData">清空</el-button>
              </el-button-group>
              <el-tooltip effect="dark" content="在页面内打开选课系统" placement="bottom">
                <el-button type="primary" @click="dialogXkVisible = true">快捷选课</el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="生成当前课表的唯一链接并保存到云端 可在任意设备上查看" placement="bottom">
                <el-button type="primary" @click="push">分享课表</el-button>
              </el-tooltip>
              <el-button-group>
                <el-button type="primary" @click="dialogAboutVisible = true">关于我们</el-button>
                <el-button type="primary" @click="shuhelper">返回主站</el-button>
              </el-button-group>
              <span style="color:grey;">已选学分</span>:{{ credit }}
            </div>
          </el-col>
        </el-row>
        <el-dialog title="16-17春季学期选课系统" v-model="dialogXkVisible" size="large">
          <el-row>
            <el-col :span="6">
              <ol>
                <li v-for="item in courseWaited" v-if="item.status=='已选入'">
                  {{ item.coursename }},{{item.teachname}},{{item.courseno}},{{item.teachno}}
                </li>
              </ol>
            </el-col>
            <el-col :span="18">
              <iframe src="http://xk.autoisp.shu.edu.cn:8080/" width="100%" height="500"></iframe>
            </el-col>
          </el-row>
  
        </el-dialog>
        <el-dialog title="分享课表" v-model="dialogShareVisible" size="small">
          <p align="center" v-if="code==''">链接生成中请耐心等待...</p>
          <p align="center" v-if="code!=''">短链接已生成，您现在可以在任何地方通过
            <a :href="'http://xk.shuhelper.cn/'+code" target="_blank">http://xk.shuhelper.cn/{{ code }}</a>访问您的课表，也可以将这个链接分享给他人。</p>
        </el-dialog>
        <el-dialog title="关于我们" v-model="dialogAboutVisible" size="small">
          <p>排课助手(xk.shuhelper.cn)是SHUhelper的一部分，主要是为了解决排课过程中的困难而制作的小工具，主要实现了搜索课程并从心仪的课程中排列出一份完美的课表的功能。</p>
          <p> 欢迎关注我们的微信公众号 搜索：
            <span style="color:red;">shuhelper</span> 或扫描下方二维码</p>
          <p align="center">
            <img width="100" src="http://static.shuhelper.cn/mp.jpg">
          </p>
          <p align="center">
            <a href="http://blog.shuhelper.cn/" target="_blank">开发博客</a>
            <a href="https://github.com/cosformula/CourseSchedulingHelper" target="_blank">开源代码</a>
          </p>
          <p align="center">
            <img src="http://forthebadge.com/images/badges/built-with-love.svg" />
            <img src="http://forthebadge.com/images/badges/uses-js.svg" />
            <img src="http://forthebadge.com/images/badges/makes-people-smile.svg" />
          </p>
          <blockquote style="color:grey;">遇到问题请加qq群：
            <span style="color:red;">368238744</span> 反馈</blockquote>
          <blockquote style="color:grey;">Version 0.8.0 | cosformula@t.shu.edu.cn | SHUhelper 开发委员会</blockquote>
          <blockquote>
            <span style="color:red;">♥</span>
            <span style="color:grey;">Do have faith in what you're doing.</span>
          </blockquote>
          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="dialogAboutVisible = false">确 定</el-button>
          </span>
        </el-dialog>
        <el-tabs type="border-card">
          <el-tab-pane label="待选课程">
            <waitcourse :courseWaited="courseWaited" @addSchedule="addSchedule" @delCourse="delCourse" />
          </el-tab-pane>
          <el-tab-pane label="搜索课程">
            <searchcourse @addCourse="addCourse" />
          </el-tab-pane>
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
  '一': 1,
  '二': 2,
  '三': 3,
  '四': 4,
  '五': 5,
}
export default {
  components: {
    Schedule,
    Waitcourse,
    Searchcourse
  },
  data () {
    return {
      courseWaited: [],
      dialogXkVisible: false,
      dialogAboutVisible: false,
      dialogVisible: false,
      dialogShareVisible: false,
      code: ''
    }
  },
  created: function () {
    var code = this.getCode()
    if (code == null) {
      this.readData()
    } else {
      this.pull(code)
    }
  },
  computed: {
    credit: function () {
      var credit = 0
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].status == '已选入') {
          credit += parseInt(this.courseWaited[i].credit)
        }
      }
      return credit
    },
    timeTable: function () {
      var table = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ]
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].status == '已选入') {
          var timelist = this.coursetimeToNum(this.courseWaited[i].coursetime)
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
    courseSelected: function () {
      console.log('courseSelected')
      var selected = [[], [], [], [], []]
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].status == '已选入') {
          var timelist = this.coursetimeToNum(this.courseWaited[i].coursetime)
          var color = [
            "#2B2E4A",
            "#521262",
            "#903749",
            "#53354A",
            "#40514E",
            "#537780",
          ]
          var course = this.courseWaited[i]
          var rancolor = color[~~(Math.random() * color.length)]
          for (var j = timelist.length - 1; j >= 0; j--) {
            var time = timelist[j]
            var item = {
              day: time.day,
              Start: time.Start,
              End: time.End,
              coursename: course.coursename,
              courseno: course.courseno,
              teachname: course.teachname,
              teachno: course.teachno,
              status: course.status,
              styleObj: {
                height: (time.End - time.Start + 1) * 7.7 + '%',
                top: ((time.Start - 1) * 7.69) + '%',
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
    getCode: function () {
      return decodeURIComponent((new RegExp('n/' + '([^&;]+?)(&|#|;|$)').exec(location.href) || [, ""])[1].replace(/\+/g, '%20')) || null
    },
    pull: function (code) {
      this.$http.get('/api/pull?code=' + code)
        .then((response) => {
          this.courseWaited = response.data
          this.$message({
            message: '已成功拉取云端的数据',
            type: 'success'
          });
        })
        .catch(function (response) {
          console.log(response)
        })
    },
    push: function () {
      this.dialogShareVisible = true
      this.code = ''
      this.$http.post('/api/push', JSON.stringify(this.courseWaited))
        .then((response) => {
          this.$message({
            message: '已成功推送数据到云端',
            type: 'success'
          });
          this.code = response.data
        })
        .catch(function (response) {
          console.log(response)
        })
    },
    query () {
      this.$http.get('/api/getcourse?courseno=' + this.form.courseno + '&coursename=' + this.form.coursename + '&teachname=' + this.form.teachname + '&coursetime=' + this.form.coursetime + '&credit=' + this.form.credit + '&campus=' + this.form.campus + '&page=' + this.page)
        .then((response) => {
          this.tableData = response.data.list
          this.total = response.data.total
        })
    },
    showDetail: function (course) {
      this.$confirm('从课表中删除' + course.coursename + course.teachname + ', 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.delCourse(course)
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
    addCourse: function (course) {
      var conflict = false
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].courseno == course.courseno && this.courseWaited[i].teachno == course.teachno) {
          conflict = true;
          break;
        }
      }
      if (conflict) {
        this.$message({
          message: '已经加入过此课程',
          type: 'warning'
        });
      }
      else {
        this.$set(course, 'status', '待加入')
        this.courseWaited.push(course)
        this.$message({
          message: '已将此课程加入待选课程列表',
          type: 'success'
        });
      }
    },
    coursetimeToNum (time) {
      var patt = /([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*/
      var timelist = []
      var str = time
      while (patt.test(str)) {
        var coursetime = patt.exec(str)
        str = str.replace(patt, "")
        var item = {
          day: parseInt(cn_num[coursetime[1]] - 1),
          Start: parseInt(coursetime[2]),
          End: parseInt(coursetime[3])
        }
        timelist.push(item)
      }
      return timelist
    },
    locateCourse (course) {
      for (var i = this.courseWaited.length - 1; i >= 0; i--) {
        if (this.courseWaited[i].courseno == course.courseno && this.courseWaited[i].teachno == course.teachno) {
          return i
        }
      }
      return -1
    },
    addSchedule: function (course) {
      //检测待加入的课程是否有冲突
      var index = this.locateCourse(course)
      var conflict = false
      var timelist = this.coursetimeToNum(this.courseWaited[index].coursetime)
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
        });
      }
      else {
        this.$set(this.courseWaited[index], 'status', '已选入')
        this.$message({
          message: '已将此课程加入课程表',
          type: 'success'
        });
      }
    },
    delCourse: function (course) {
      var index = this.locateCourse(course)
      console.log('delcourse')
      if (course.status == '已选入') {
        this.$set(this.courseWaited[index], 'status', '待加入')
      }
      else {
        this.courseWaited.splice(index, 1)
      }
      this.$message({
        message: '已成功删除该课程',
        type: 'success'
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
      if (JSON.parse(localStorage.getItem('courseWaited'))) {
        this.courseWaited = JSON.parse(localStorage.getItem('courseWaited'))
        this.$message({
          message: '已成功读取上次的数据',
          type: 'success'
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
      this.$confirm('此操作将删除目前的选课结果且无法恢复, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
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
      window.open('https://www.shuhelper.cn/')
    }
  }
}
</script>

<style>
body {
  font-family: Helvetica, sans-serif;
}

html,
body {
  height: 100%;
  margin: 0;
}

#app {
  height: 100%;
}
</style>
