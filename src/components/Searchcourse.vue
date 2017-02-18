<template>
<div  @keyup.enter="onsubmit">
    <el-form :inline="true" ref="form" :model="form" label-width="70px">
    <el-form-item label="课程号">
        <el-input v-model="form.courseno" ></el-input>
    </el-form-item>
    <el-form-item label="课程名">
        <el-input v-model="form.coursename"></el-input>
    </el-form-item>
    <el-form-item label="教师名">
        <el-input v-model="form.teachname"></el-input>
    </el-form-item>
    <el-form-item label="学分">
        <el-input v-model="form.credit"></el-input>
    </el-form-item>
    <el-form-item label="上课时间">
        <el-input placeholder="格式：一1-2" v-model="form.coursetime"></el-input>
    </el-form-item>
    <el-form-item label="校区">
    <el-select v-model="form.campus" placeholder="请选择校区">
      <el-option label="全部" value=""></el-option>
      <el-option label="本部" value="本部"></el-option>
      <el-option label="嘉定" value="嘉定"></el-option>
      <el-option label="延长" value="延长"></el-option>
    </el-select>
    </el-form>
    <el-table
    :data="tableData"
    highlight-current-row
    border
    height="400"
    style="width: 100%">
    <el-table-column
      label="课程名"
      width="200">
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
      </template>
    </el-table-column>
    <el-table-column
      prop="teachname"
      label="教师"
      width="80">
    </el-table-column>
    <el-table-column
      prop="courseno"
      label="课程号"
      width="100">
    </el-table-column>
    <el-table-column
      prop="credit"
      label="学分"
      width="80">
    </el-table-column>
    <el-table-column
      prop="coursetime"
      label="时间"
      width="150">
    </el-table-column>
    <el-table-column
      label="人数"
      width="100">
       <template scope="scope">
       {{ scope.row.enroll}}/{{ scope.row.capacity}}
      </template>
    </el-table-column>
    <el-table-column
      prop="campus"
      label="校区"
      width="80">
    </el-table-column>
    
    <el-table-column label="操作" fixed="right">
      <template scope="scope">
        <el-button
          size="small"
          @click="addWait(scope.$index, scope.row)">加入待选课程</el-button>
      </template>
    </el-table-column>
    </el-table>
     <el-pagination
      layout="total, prev, pager, next, jumper"
      :page-size="50"
      :total="total"
      :current-page="page"
      @current-change="handlePageCurrentChange">
    </el-pagination>

</div>
</template>
<script>
  export default {
    data() {
      return {
        tableData:[],
        form: {
          courseno: '',
          coursename: '',
          teachname: '',
          credit: '',
          coursetime: '',
          campus:'',
        },
        page:1,
        currentRow: null,
        scroll: true,
        total: 0,
        searchQueryIsDirty: false
      }
    },
    created:function (){
      this.query() 
    },
    watch:{
      form:{
        handler: function () {
          this.searchQueryIsDirty = true
          this.onFormChange()
        },
        deep: true
      }
    },
    methods: {
      onFormChange: _.debounce(function () {
        this.onSubmit()
        this.searchQueryIsDirty = false
      }, 500),
      onSubmit() {
        this.page = 1
        this.query()
      },
      handlePageCurrentChange(val) {
        this.page = val
        this.tableData = []
        this.query()
      },
      query(){
        this.$http.get('/api/getcourse?courseno='+this.form.courseno+'&coursename='+this.form.coursename+'&teachname='+this.form.teachname+'&coursetime='+this.form.coursetime+'&credit='+this.form.credit+'&campus='+this.form.campus+'&page='+this.page)
            .then((response) => {
                        this.tableData = response.data.list
                        this.total = response.data.total
                    })
      },
      handleCurrentChange(val) {
        this.currentRow = val;
      },
      addWait(index,row){
          this.$emit('addCourse',row)
      }
    }
  }
</script>