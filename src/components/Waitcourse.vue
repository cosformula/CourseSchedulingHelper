<template>
  <el-table
    :data="courseWaited"
    highlight-current-row
    height="500"
    border
    style="width: 100%">
    <el-table-column
      label="课程名"
      width="200"
      sortable>
    <template scope="scope">
        <el-popover trigger="hover" placement="left">
        <p>课程名: {{ scope.row.coursename }}</p>
        <p>课程号: {{ scope.row.courseno }}</p>
        <p>教师名: {{ scope.row.teachname }}</p>
        <p>教师号: {{ scope.row.teachno }}</p>
        <p>选课人数: {{ scope.row.enroll }}/{{ scope.row.capacity }}</p>
        <p>开课学院: {{ scope.row.school }}</p>
        <p>标签: {{ scope.row.tag }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag>{{ scope.row.coursename }}</el-tag>
          </div>
        </el-popover>
    </el-table-column>
    <el-table-column
      prop="teachname"
      label="教师"
      width="100"
      sortable>
    </el-table-column>
    <el-table-column
      prop="coursetime"
      label="时间"
      width="100"
      sortable>
    </el-table-column>
    <el-table-column
      prop="enroll"
      label="人数"
      width="90"
      sortable>
    </el-table-column>
    <el-table-column
      prop="status"
      label="状态"
      width="90"
      sortable>
    </el-table-column>
    <el-table-column label="操作">
      <template scope="scope">
        <el-button
          size="small"
          v-if="scope.row.status=='待加入'"
          @click="addSchedule(scope.row)">加入课程表</el-button>
        <el-button
          size="small"
          type="danger"
          @click="delCourse(scope.row)">{{scope.row.status=='待加入'?'从待选课程中删除':'从课表中删除'}}</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
  export default {
   props: {
      courseWaited:{
          type: Array,
          default(){
              return []
          }
      }
    },
    data() {
      return {
        
      }
    },
    methods:{
        addSchedule:function(row){
          this.$emit('addSchedule',row)
        },
        delCourse:function(row){
          console.log(row)
          this.$emit('delCourse',row)
        }
    }
  }
</script>