<template>
  <el-table
    :data="courseWaited"
    highlight-current-row 
    max-height="700"
    border>
    <el-table-column label="操作"   width="150">
      <template scope="scope">
        <el-tooltip effect="dark" content="添加到课表" placement="left">
           <el-button
                  size="small"
                  v-if="scope.row.status=='待加入'"
                  @click="addSchedule(scope.row)"
                  icon="el-icon-circle-plus"></el-button>
        </el-tooltip>
        <el-tooltip  effect="dark" :content="scope.row.status=='待加入'?'删除':'从课表删除'" placement="right">
          <el-button
          size="small"
          type="danger"
          icon="el-icon-remove-outline"
          @click="delCourse(scope.row)"></el-button>
        </el-tooltip>
      </template>
    </el-table-column>
    <el-table-column
      label="课程名"
      width="150">
    <template scope="scope">
        <el-popover trigger="hover" placement="right">
        <p>课程名: {{ scope.row.course_name }}</p>
        <p>课程号: {{ scope.row.course_no }}</p>
        <p>教师名: {{ scope.row.teacher_name }}</p>
        <p>教师号: {{ scope.row.teacher_no }}</p>
        <p>选课人数: {{ scope.row.enroll }}/{{ scope.row.capacity }}</p>
        <p>开课学院: {{ scope.row.school }}</p>
        <p>标签: {{ scope.row.tag }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag>{{ scope.row.course_name }}</el-tag>
          </div>
        </el-popover>
    </template>
    </el-table-column>
    <el-table-column
      label="教师"
      width="80">
      <template slot-scope="scope">
        <span style="white-space:nowrap;"> {{ scope.row.teacher_name }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="credit" label="学分" width="89" sortable>
    </el-table-column>
    <el-table-column
      prop="time"
      label="时间"
      width="100"
      sortable>
    </el-table-column>
    <el-table-column prop="enroll" label="人数" width="90" sortable>
    </el-table-column>
    <el-table-column prop="capacity" label="容量" width="90" sortable>
    </el-table-column>
    <el-table-column
      prop="status"
      label="状态"
      width="100"
      sortable>
    </el-table-column>

  </el-table>
</template>

<script>
export default {
  props: {
    courseWaited: {
      type: Array,
      default() {
        return []
      }
    }
  },
  data() {
    return {}
  },
  methods: {
    addSchedule: function(row) {
      this.$emit('addSchedule', row)
    },
    delCourse: function(row) {
      console.log(row)
      this.$emit('delCourse', row)
    }
  }
}
</script>
<style>
.el-tabs__content {
  height: 100%;
}
</style>
