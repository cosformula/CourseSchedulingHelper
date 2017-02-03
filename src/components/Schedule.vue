<template>
    <div class="schedule">
    	<div class="time-ground">
				<div style="height:49.2px;"></div>
				<div v-for="time in timeGround" style="height:49.2px;margin:0">
				<span>{{time}}</span>
				</div>
    	</div>
    	<div class="task-ground">
				<div v-for="(week,index) in weekGround" class="task-list">
    				<div style="height:50px;">
						<p style="margin:0;padding-top:15px;">{{week}}</p>
						</div>
    				<div :style="taskListSty">
              <div class="task-list-item" 
                  v-for="detail in taskDetail[index]" 
                  :style="detail.styleObj" 
                  @click="showDetail(detail, week)">
                <div>
    						<h5>{{detail.title}}</h5>
                <p>{{detail.teacher}}</p>
                </div>
    					</div>
    				</div>
    			</div>
    	</div>
    	<modal :show.sync="showModal" :show-modal-detail.sync="showModalDetail" @close="closeModal">
    </div>
</template>

<style scoped>
	.schedule{
		width: 90%;
		max-width: 1400px;
		margin: 0 auto;
		position: relative;
	}
	.time-ground{
		display: block;
		position: absolute;
		left: 0;
		top: 0;
		width: 100%;
	}
	.time-ground div{
		border-bottom-style:solid;
		border-color:#EAEAEA;
		border-width:1px;
	}
	.time-ground div span{
		position: relative;
		left:-20px;
		top:20px;
	}
	.task-ground{
		width: 100%;
	}
	.task-list{
		float: left;
		width: 20%;
		box-sizing:border-box;
		border:1px solid #EAEAEA;
	}
	.task-list p{
		text-align: center;
		font-size: 0.9rem;

	}
	.task-list-item{
		position: absolute;
		background-color: #577F92;
		width: 20%;
		cursor: pointer;
    text-align: center;
    vertical-align:middle;
	}
	.task-list-item p{
		padding: 0;
		font-size: 0.8rem;
		color: #EDF2F6;
    margin-bottom: 0.5rem;
	}
	.task-list-item h5{
		color: #E0E7E9;
	}
	ul{
		list-style-type:none;
	}
</style>

<script>

import Modal from './Modal.vue';


export default {
	props: {
		timeGround: {
      default() {
        return[
						"1",
						"2",
						"3",
						"4",
						"5",
						"6",
						"7",
						"8",
						"9",
						"10",
            "11",
            "12",
            "13"
					]
      }
		},
		weekGround: {
			type: Array,
      default() {
        return [
				'周一',
				'周二',
				'周三',
				'周四',
				'周五'
        ]  
      }
		},
		taskDetail: {
			type: Array,
			default: []
		},
		color: {
			type: Array,
			default(){
				return [
					"#2B2E4A",
					"#521262",
					"#903749",
					"#53354A",
					"#40514E",
					"#537780",
				]

			}
		}
	},
	components: {
		Modal: Modal
	},
	data() {
		return {
			showModal: false,
			showModalDetail: {
				dateStart: '09:30',
				dateEnd: '10:30',
				title: 'Metting',
				week: 'Monday',
				styleObj: {
					backgroundColor: "#0000"
				},
				detail: 'Metting (German: Mettingen) is a commune in the Moselle department in Grand Est in north-eastern France.'
			},
			taskListSty: {
				height: '650px'
			}
		}
	},
	compiled() {
		this.taskListSty.height = (this.timeGround.length - 1) * 100 + 'px';
	},
	methods: {
		showDetail(obj, week){
			obj.week = week;
			this.showModalDetail = obj;
			this.showModal = true;
		},
    closeModal:function () {
      this.showModal = false
    }
    
	}
}
</script>